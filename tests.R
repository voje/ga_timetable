run_tests <- function() {
  for (i in 1:GA@popSize) {
    cat(my_fitness_function(GA@population[i,]), "\n");
  }
}

test_generate_chromosome <- function() {
  res <- numeric();
  for (i in 1:1000) {
    print(i);
    new <- helper_is_legit_participant(helper_create_chromosome(mapping_matrix));
    res <- c(res, new);
  }
  return(res);
}

test_my_crossover <- function(N=1000) {
  tests <- numeric();
  for (i in 1:N) {
    cat("\r", i);
    p1 <- helper_create_chromosome(mapping_matrix);
    p2 <- helper_create_chromosome(mapping_matrix);
    GA@population[1,] <- p1;
    GA@population[2,] <- p2;
    res <- my_crossover(GA, c(1,2));
    rc1 <- helper_is_legit_participant(res$children[1,]);
    rc2 <- helper_is_legit_participant(res$children[2,]);
    t1 <- (rc1 & rc2);
    tests <- c(tests, t1);
  }
  return(tests);
}