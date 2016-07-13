helper_create_chromosome <- function(mapping_matrix) {
  chr <- numeric();
  for (i in 1:nrow(mapping_matrix)) {
    quadruple <- which(mapping_matrix[i,] == 1);
    quadruple <- sample(quadruple);
    for (j in 1:length(quadruple)) {
      chr <- c(chr, decimal2binary(quadruple[j], 4));
    }
  }
  return(chr);
}

helper_chromosome_to_decimal <- function(chromosome) {
  dec <- numeric();
  for (i in 1:(length(chromosome)/4)) {
    idx <- (i-1)*4+1;
    idx1 <- idx+3;
    num <- chromosome[idx:idx1];
    #cat(num, "\n");
    dec <- c(dec, binary2decimal(num));
  }
  return(dec);
}

helper_decimal_to_chromosome <- function(decimal) {
  chromosome <- numeric();
  for (i in 1:length(decimal)) {
    bin <- decimal2binary(decimal[i], 4);
    chromosome <- c(chromosome, bin);
  }
  return(chromosome);
}

helper_is_legit_participant <- function(x, binary=TRUE) {
  #critical condition (participant in the right workshops)
  if (binary) {
    dec <- helper_chromosome_to_decimal(x);
  } else {
    dec <- x;
  }
  for (i in 1:(length(dec)/4)) {
    #i is the index of the participant
    idx <- (i-1)*4+1;
    idx1 <- idx+3;
    child <- dec[idx:idx1];
    for (j in 1:length(child)) {
      #check if child is in the right workshop
      if (child[j] < 1 || child[j] > 11) {
        return(FALSE);
      }
      if (mapping_matrix[i,child[j]] == 0) {
        return(FALSE);
      }
    }
  }
  return(TRUE);
}

helper_normalize <- function(val, in_interval) {
  e <- (in_interval[2]-in_interval[1])/100;
  n <- (val - in_interval[1]) / e;
  if (n > 100) {
    n <- 100;
  } else if (n < 0) {
    n <- 0;
  }
  return(n);
}



