package com.ir.createIndex;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.ParseException;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.search.similarities.BM25Similarity;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class BM25Computer {
    private static Analyzer analyzer = new StandardAnalyzer(Version.LUCENE_47);
    private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    private IndexWriter writer;
    private ArrayList<File> queue = new ArrayList<File>();
    private String indexDir;
    Set<String> stopwordSet;

    /**
     * Constructor
     * 
     * @param indexDir
     *            the name of the folder in which the index should be created
     * @throws java.io.IOException
     *             when exception creating index.
     */
    BM25Computer(String indexDir) throws IOException {
    	this.indexDir = indexDir;
    	
		FSDirectory dir = FSDirectory.open(new File(indexDir));
	
		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
			analyzer);
		config.setSimilarity(new BM25Similarity()); // set to use BM25 (default k1 = 1.2, b = 0.75)
		
		writer = new IndexWriter(dir, config);
		
		stopwordSet = new HashSet<String>();
		List<String> stopwordList = Arrays.asList();
		//stopwordSet.addAll(c)
    }

    /**
     * Indexes a file or directory
     * 
     * @param fileName
     *            the name of a text file or a folder we wish to add to the
     *            index
     * @throws java.io.IOException
     *             when exception
     */
    public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));
	
		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
		    FileReader fr = null;
		    try {
			Document doc = new Document();
	
			// ===================================================
			// add contents of file
			// ===================================================
			fr = new FileReader(f);			
			doc.add(new TextField("contents", fr));
			doc.add(new StringField("path", f.getPath(), Field.Store.YES));
			doc.add(new StringField("filename", f.getName(),
				Field.Store.YES));
	
			writer.addDocument(doc);
			System.out.println("Added: " + f);
		    } catch (Exception e) {
			System.out.println("Could not add: " + f);
		    } finally {
			fr.close();
		    }
		}
	
		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out
			.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");
	
		queue.clear();
    }

    private void addFiles(File file) {
		if (!file.exists()) {
		    System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
		    for (File f : file.listFiles()) {
			addFiles(f);
		    }
		} else {
		    String filename = file.getName().toLowerCase();
		    // ===================================================
		    // Only index text files
		    // ===================================================
		    if (filename.endsWith(".htm") || filename.endsWith(".html")
			    || filename.endsWith(".xml") || filename.endsWith(".txt")) {
			queue.add(file);
		    } else {
			System.out.println("Skipped " + filename);
		    }
		}
    }

    /**
     * Close the index.
     * 
     * @throws java.io.IOException
     *             when exception closing
     */
    public void closeIndex() throws IOException {
    	writer.close();
    }
  
    /**
     * create index for docs in the given location
     * @param docsDir
     * @throws IOException
     */
    public void indexingDocs(String docsDir) throws IOException {
    	// add docs for indexing
	    try {
	    	indexFileOrDirectory(docsDir);
	    } catch (Exception e) {
	    	System.out.println("Error indexing " + docsDir + " : " + e.getMessage());
	    }
	    
		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		closeIndex();
    }
    
    /**
     * query given term in the index, write top k results into given location
     * @param queryTerm, terms need to query
     * @param topK, number of top results
     * @param resultDir, location of saving results
     */
    public void query(int queryId, String queryTerm, int topK, String resultDir) throws IOException, ParseException {
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(this.indexDir)));
		TopScoreDocCollector collector = TopScoreDocCollector.create(topK, true); 
		IndexSearcher searcher = new IndexSearcher(reader);
		searcher.setSimilarity(new BM25Similarity()); // set searcher to use BM25 (default k1 = 1.2, b = 0.75)
		
	
		System.out.println("Tofile:///home/tong/ProgramFile/eclipseProjects/.metadata/.plugins/org.eclipse.jdt.ui/jdt-images/0.pngp " + topK + " results for querying [" + queryTerm + "] :");
		
		// query top results based on the default score compfile:///home/tong/ProgramFile/eclipseProjects/.metadata/.plugins/org.eclipse.jdt.ui/jdt-images/4.pngutation
		Query q = new QueryParser(Version.LUCENE_47, "contents",analyzer).parse(queryTerm);
		searcher.search(q, collector);
		ScoreDoc[] hits = collector.topDocs().scoreDocs;
	    
		// write results to file
		StringBuilder sb = new StringBuilder();
		sb.append("query_id,Q0,duc_id,rank,BM25_score,System_name\n");
		for (int i = 0; i < hits.length; ++i) {
		    int docId = hits[i].doc;
	    	
		    //System.out.println("doc id: " + docId);
		    Document d = searcher.doc(docId);
		    String docName = d.get("filename").split(".txt")[0];
		    double docScore = hits[i].score;
		    
		    sb.append(queryId + "," + "Q0," + docName + "," + String.valueOf(i + 1) + "," + docScore + ",Lucene" + "\n");
		    //System.out.println((i + 1) + ". " + "name=" + docName + " score=" + docScore);
		}
		
		BufferedWriter bwr = new BufferedWriter(new FileWriter(new File(resultDir)));
		bwr.write(sb.toString());
		bwr.flush();
		bwr.close();
    }
    
    
    public static void main(String[] args) throws IOException, ParseException {
    	String INDEX_DIR = "/home/tong/ProgramFile/eclipseProjects/createIndex/index";
    	String DOCS_DIR = "/home/tong/ProgramFile/eclipseProjects/createIndex/docs";
    	String RESULT_DIR = "/home/tong/ProgramFile/eclipseProjects/createIndex/hw4-result"; // result without expansion
    	
    	String indexDir = INDEX_DIR;
    	String docsDir = DOCS_DIR;

    	// create indexer with given index location
    	BM25Computer indexer = null;
		try {
		    indexer = new BM25Computer(indexDir);
		} catch (Exception ex) {
		    System.out.println("Cannot create index..." + ex.getMessage());
		    System.exit(-1);
		}

		// indexing docs
		// indexer.indexingDocs(docsDir);
		
		// query without expansion
		List<String> queryList = Arrays.asList("milky way galaxy", "hubble space telescope", "international space station", "big bang theory", "mars exploratory missions");
		for (int i = 0; i < queryList.size(); i++) {
			String queryTerm = queryList.get(i);
	    	String queryTermDir = queryTerm.toLowerCase().replace(' ', '-');
	    	String resultDir = RESULT_DIR + "/" + "query" + (i + 1) + ".csv";
			indexer.query(i + 1, queryTerm, 100, resultDir); // query top 100 results for given term	
		}
    }
}