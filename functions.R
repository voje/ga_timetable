get_grade <- function(factor) {
  str <- as.character(factor);
  grd <- as.integer(substring(str, 1, 1));
  return(grd);
}

create_participants_vector <- function(data) {
  l <- unlist(data, use.names=F);
  ul <- unique(l);
  sl <- as.character(ul);
  sl1 <- sl[sl!=""];
  ssl <- sort(sl1);
  f <- as.factor(ssl);
  cat("Number of participants: ", length(f));
  return(f);
}

create_activities_vector <- function(data) {
   n <- as.factor(names(data));
   return(n);
}

create_mapping_matrix <- function(participants, activities, data) {
  m <- matrix(0, nrow=length(participants), ncol=length(activities));
  rownames(m) <- participants;
  colnames(m) <- activities;
  #fill in values
  for (activity in activities) {
    col <- data[,activity];
    for (participant in col) {
      if (participant != "") {
        m[participant, activity] = 1;
      }
    }
  }
  return(m);
}

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

my_init_pop <- function(object) {
  if (!exists("mapping_matrix")) {
    return(FALSE);
  }
  n_iter <- object@popSize;
  m <- numeric();
  for (i in 1:n_iter) {
    m <- rbind(m, helper_create_chromosome(mapping_matrix));
  }
  return(m);
}

get_nBits <- function(mapping_matrix) {
  n <- nrow(mapping_matrix);
  return(n*4*4);
}

my_fitness_function <- function(x) {
  #convert chromosome to decimal values
  dec <- helper_chromosome_to_decimal(x);

  #critical condition (participant in the right workshops)
  for (i in 1:(length(dec)/4)) {
    #i is the index of the participant
    idx <- (i-1)*4+1;
    idx1 <- idx+3;
    child <- dec[idx:idx1];
    for (j in 1:length(child)) {
      #check if child is in the right workshop
      if (child[j] < 1 || child[j] > 11) {
        return(-1000);
      }
      if (mapping_matrix[i,child[j]] == 0) {
        return(-1000);
      }
    }
  }
  
  #check variance of workshop participands, check variances of ages per workshop
  mat <- matrix(nrow=length(participants), ncol=4*11);
  for (i in 1:(length(dec)/4)) {
    #i is the index of the participant
    idx <- (i-1)*4+1;
    idx1 <- idx+3;
    child <- dec[idx:idx1];
    for (j in 1:length(child)) {
      #workshop index (4 * 11 workshops)
      widx <- (j-1)*11 + child[j];
      mat[i, widx] <- get_grade(participants[i]);
    }
  }
  
  #variance of participants per workshop
  part_per_workshop <- numeric();
  for (i in 1:length(mat[1,])) {
    col <- mat[,i];
    selection <- col[!is.na(col)];
    #if too few, discard
    if (length(selection) < 2) {
      return(-1000);
    }
    s <- sum(selection);
    part_per_workshop <- c(part_per_workshop, s);
  }
  partic_var <- var(part_per_workshop);
  
  #variance of ages in an individual workshop
  age_var_per_workshop <- numeric();
  for(i in 1:length(mat[1,])) {
    col <- mat[,i];
    selection <- col[!is.na(col)];
    v <- var(selection);
    age_var_per_workshop <- c(age_var_per_workshop, v);
  }
  age_score <- sum(age_var_per_workshop);
  
  if (!exists("age_weight")) {
    age_weight = 1;
    num_weight = 1;
  }
  
  return((-1)*(partic_var*num_weight + age_score*age_weight));
}

pretty_table <- function(chr) {
  dec <- helper_chromosome_to_decimal(chr);
  #groups participants by workshops
  ncols <- 11*4;
  nrows <- length(participants);
  rmat <- matrix(ncol=ncols, nrow=nrows);
  colnames(rmat) <- rep(activities, 4);
  tmp_counter <- rep(1, ncols);
  for (i in 1:(length(dec)/4)) {
    #i is the index of the participant
    idx <- (i-1)*4+1;
    idx1 <- idx+3;
    child <- dec[idx:idx1];
    for (j in 1:length(child)) {
      #workshop index (4 * 11 workshops)
      widx <- (j-1)*11 + child[j];
      rmat[tmp_counter[widx], widx] <- as.character(participants[i]);
      tmp_counter[widx] <- tmp_counter[widx] + 1;
    }
  }
  return(rmat);
}

my_crossover <- function(object, parents) {
  parent1 <- object@population[parents[1],];
  parent2 <- object@population[parents[2],];
  
  n_participants <- length(parent1)/16;
  
  #how many participants are on the left side of the cut (1:all-1)
  cutter <- sample(1:(n_participants-1), 1)*16;
  #parent1
  c1 <- parent1[1:cutter];
  c2 <- parent1[(cutter+1):length(parent1)];
  #parent2
  c3 <- parent2[1:cutter];
  c4 <- parent2[(cutter+1):length(parent2)];
  
  #children
  child1 <- c(c1, c4);
  child2 <- c(c3, c2);
  
  val_c1 <- my_fitness_function(child1);
  val_c2 <- my_fitness_function(child2);
  
  res <- list();
  mat <- matrix(c(child1, child2), ncol=length(child1));
  res$children <- mat;
  res$fitness <- c(val_c1, val_c2);

  return(res);
}

my_mutation <- function(object, parent_idx) {
  parent <- object@population[parent_idx,];
  #cat(dim(parent));
  n_participants <- length(parent)/16;
  pidx <- sample(1:n_participants, 1);
  pos <- (pidx-1)*16 + 1;
  pos1 <- pos+15;
  bin <- parent[pos:pos1];
  dec <- helper_chromosome_to_decimal(bin);
  dec <- sample(dec);
  bin <- helper_decimal_to_chromosome(dec);
  parent[pos:pos1] <- bin;
  return(parent);
}

run_tests <- function() {
  for (i in 1:GA@popSize) {
    cat(my_fitness_function(GA@population[i,]), "\n");
  }
}