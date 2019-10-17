url <- "C:\\Users\\manzh\\anaconda3\\Lib\\site-packages\\SEC-Edgar-Data\\ETSY\\0001370637\\8-K\\0001193125-19-252365.txt"
exploreDoc <- try(readLines(url))

cleanedDoc <- gsub("<.*?>", "", exploreDoc)
cleanedDoc <- gsub("&nbsp;"," ", cleanedDoc)
cleanedDoc <- gsub(" {2,}", "", cleanedDoc)
cleanedDoc <- gsub("^\\s+|\\s+$", "", cleanedDoc)
cleanedDoc <- gsub("\\d+", "", cleanedDoc)
cleanedDoc <- gsub("&#;", "", cleanedDoc)
cleanedDoc <- gsub("[^[:alnum:][:blank:]+?&/\\-]", "", cleanedDoc)
cleanedDoc <- cleanedDoc[cleanedDoc != ""]
cleanedDoc <- cleanedDoc[cleanedDoc != " "]
cleanedDoc <- cleanedDoc[cleanedDoc != ",,"]
cleanedDoc <- cleanedDoc[cleanedDoc != ","]

write.table(cleanedDoc,file = 'C:/data/CS/project3/cleandoc2.txt',sep = ' ')
