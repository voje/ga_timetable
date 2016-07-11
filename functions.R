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