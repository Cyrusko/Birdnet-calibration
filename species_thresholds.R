options(repos = c(CRAN = "https://cloud.r-project.org/"))
for(pkg in c("dplyr","broom","readr","tidyr")) {
  if(!requireNamespace(pkg, quietly=TRUE)) install.packages(pkg)
}
library(dplyr); library(broom); library(readr); library(tidyr)

# 1. Read in your validated CSV
raw <- read_delim(
  "validated_birdnet.csv",
  delim = ";",
  trim_ws = TRUE,
  col_types = cols(
    species     = col_character(),
    confidence  = col_double(),
    `Validation Status` = col_skip(),
    label       = col_double()
  )
) %>%
  mutate(label = as.integer(label))

# 2. Prepare the output table
results <- tibble(
  species      = character(),
  threshold    = double(),
  precision    = double(),
  retained_pct = double()
)

# 3. Only search thresholds from 0.50 to 1.00
conf_vals <- seq(0.5, 1.0, by = 0.01)

# 4. Loop species
for(sp in unique(raw$species)) {
  sub <- filter(raw, species == sp)
  if(n_distinct(sub$label) < 2) next

  # Fit logistic model
  fit <- glm(label ~ confidence, data = sub, family = binomial)

  # Predict P(true positive) at each conf_val
  tpr_vals <- predict(fit, newdata = tibble(confidence = conf_vals), type = "response")

  # Count how many detections in each bin
  bin_counts <- sub %>%
    mutate(conf_bin = round(confidence, 2)) %>%
    count(conf_bin) %>%
    complete(conf_bin = conf_vals, fill = list(n = 0))

  # Evaluate precision and retention
  eval_df <- tibble(threshold = conf_vals) %>%
    rowwise() %>%
    mutate(
      TP = sum(tpr_vals[conf_vals >= threshold] * bin_counts$n[conf_vals >= threshold]),
      FP = sum((1 - tpr_vals[conf_vals >= threshold]) * bin_counts$n[conf_vals >= threshold]),
      total = sum(bin_counts$n[conf_vals >= threshold]),
      precision    = if_else((TP + FP) > 0, TP / (TP + FP), NA_real_),
      retained_pct = 100 * total / sum(bin_counts$n)
    ) %>%
    ungroup()

  # Pick the smallest threshold giving ≥90% precision
  best <- eval_df %>%
    filter(!is.na(precision) & precision >= 0.9) %>%
    slice_min(threshold, with_ties = FALSE)

  if(nrow(best) == 0) {
    best <- eval_df %>%
      slice_max(threshold, with_ties = FALSE)
  }

  results <- bind_rows(
    results,
    tibble(
      species      = sp,
      threshold    = best$threshold,
      precision    = best$precision,
      retained_pct = best$retained_pct
    )
  )
}

# 5. Write out your new thresholds
write_csv(results, "species_specific.csv")
message("Wrote species_specific.csv for ", nrow(results), " species.")
