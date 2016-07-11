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

eval_function <- function(x) {
  #this is where things get fun
  
}









