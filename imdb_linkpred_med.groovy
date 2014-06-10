package edu.umd.cs.imdb;

import edu.umd.cs.psl.application.inference.LazyMPEInference;
import edu.umd.cs.psl.application.learning.weight.maxlikelihood.LazyMaxLikelihoodMPE;
import edu.umd.cs.psl.config.*
import edu.umd.cs.psl.database.DataStore
import edu.umd.cs.psl.database.Database;
import edu.umd.cs.psl.database.Partition;
import edu.umd.cs.psl.database.ReadOnlyDatabase;
import edu.umd.cs.psl.database.rdbms.RDBMSDataStore
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver
import edu.umd.cs.psl.database.rdbms.driver.H2DatabaseDriver.Type
import edu.umd.cs.psl.groovy.PSLModel;
import edu.umd.cs.psl.groovy.PredicateConstraint;
import edu.umd.cs.psl.groovy.SetComparison;
import edu.umd.cs.psl.model.argument.ArgumentType;
import edu.umd.cs.psl.model.argument.GroundTerm;
import edu.umd.cs.psl.model.atom.GroundAtom;
import edu.umd.cs.psl.model.function.ExternalFunction;
import edu.umd.cs.psl.ui.functions.textsimilarity.*
import edu.umd.cs.psl.ui.loading.InserterUtils;
import edu.umd.cs.psl.util.database.Queries;


ConfigManager cm = ConfigManager.getManager()
ConfigBundle config = cm.getBundle("imdb")

/* Uses H2 as a DataStore and stores it in a temp. directory by default */
def defaultPath = System.getProperty("java.io.tmpdir")
String dbpath = config.getString("dbpath", defaultPath + File.separator + "imdb")
DataStore data = new RDBMSDataStore(new H2DatabaseDriver(Type.Disk, dbpath, true), config)


PSLModel m = new PSLModel(this, data)

m.add predicate:"collaboration", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
 //collaboration, open predicate

m.add predicate:"observedcollaboration", types : [ArgumentType.UniqueID, ArgumentType.UniqueID] 
//observed actor collaborations, closed predicate
//all subsequent predicates are side features and are closed
m.add predicate:"directed", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
m.add predicate:"genre", types: [ArgumentType.UniqueID, ArgumentType.String]
m.add predicate:"language", types: [ArgumentType.UniqueID, ArgumentType.String]
m.add predicate:"dead", types: [ArgumentType.UniqueID]
m.add predicate:"produced", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
m.add predicate:"gender", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
m.add predicate:"actorprodcompany", types: [ArgumentType.UniqueID, ArgumentType.String]//actor- production company collaboration
m.add predicate:"actordistcompany", types: [ArgumentType.UniqueID, ArgumentType.String]//actor- distribution company collaboration
m.add predicate:"actorquality", types: [ArgumentType.UniqueID, ArgumentType.Double]
// quality of actors based on average rating of movies they have starred

m.add function: "sameGenre" , implementation: new ExactMatch()
m.add function: "sameLanguage" , implementation: new ExactMatch()
m.add function: "similarquality", implementation: new SimilarQuality()
 // considers quality similar when it differs no more than 0.8 (arbitrary)

// Use block only for extra large dataset, add block conjuncts to rules i.e. BLOCK(X,Y)
m.add predicate:"block", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]

//m.add predicate:"inferredcollaboration", types: [ArgumentType.UniqueID, ArgumentType.UniqueID]
//m.add rule : (observedcollaboration(X,Y)) >> collaboration(X,Y), weight : 10.0
m.add rule : ( (X-Z) & observedcollaboration(X,Y) & observedcollaboration(Y,Z) ) >> collaboration(X,Z), weight : 0.01
m.add rule:  (dead(A))>> ~collaboration(A,F), weight: 10
m.add rule: (genre(A,B) & genre(C,D) & (A-C) & ~observedcollaboration(A,C) & sameGenre(B,D)) >> collaboration(A,C), weight : 0.0001

m.add rule: (language(A,B) & language(C,D) & (A-C) & ~observedcollaboration(A,C) & sameLanguage(B,D)) >> collaboration(A,C), weight : 0.0001
//m.add rule : ( (X-Z) & observedcollaboration(X,Y) & observedcollaboration(Y,Z)
//	& observedcollaboration(X,Q) & observedcollaboration(Y,Q) & (Y-Q) ) >> collaboration(X,Z), weight : 1.5

m.add rule : ( observedcollaboration(X,Y) & ~observedcollaboration(Y,Z) ) >> ~collaboration(X,Z), weight : 10.0 --negative rule
//m.add rule : ( ~observedcollaboration(X,Y) & observedcollaboration(Y,Z) ) >> ~collaboration(X,Z), weight : 0.5

m.add rule: (directed(C,D) & (C ^ D) & directed(C,E) & (C ^ E ) & ~observedcollaboration(D,E) ) >> collaboration(D,E), weight : 0.2
m.add rule: (produced(C,D) & (C ^ D) & produced(C,E) & (C ^ E ) & ~observedcollaboration(D,E) ) >> collaboration(D,E), weight : 0.2

m.add rule: (actorprodcompany(D,C) & (D ^C ) & actorprodcompany(E,C) & (E ^ C) & ~observedcollaboration(D,E) ) >> collaboration(D,E), weight : 0.02

m.add rule: (actorprodcompany(D,C) & (D ^C ) & actorprodcompany(E,C) & (E ^ C) & ~observedcollaboration(D,E) ) >> collaboration(D,E), weight : 0.02

m.add rule: (actorquality(A,B) & actorquality(C,D) & (A-C) & ~observedcollaboration(A,C) & similarquality(B,D)) >> collaboration(A,C), weight : 5.0


m.add PredicateConstraint.Symmetric, on : collaboration
m.add PredicateConstraint.Symmetric, on : observedcollaboration
//m.add PredicateConstraint.Nonsymmetric , on : directed


println m;


/*
 * We now insert data into our DataStore. All data is stored in a partition.
*/

//loading all the files with the side features into partition 0
def partition = new Partition(0);
def insert = data.getInserter(directed, partition);
def dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/DA20012005med.tsv");

insert = data.getInserter(produced, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/PA20012005med.tsv");

insert = data.getInserter(genre, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AG20012005med.tsv");

insert = data.getInserter(language, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AL20012005med.tsv");

insert = data.getInserter(dead, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/Dead20012005med.tsv");

insert = data.getInserter(gender, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/Gender20012005med.tsv");

insert = data.getInserter(actorprodcompany, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AP20012005med.tsv");

insert = data.getInserter(actordistcompany, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AD20012005med.tsv");

insert = data.getInserter(actorquality, partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AQ20012005med.tsv");


insert = data.getInserter(observedcollaboration, partition)
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/C0105med.tsv");
System.out.println("Here");


insert = data.getInserter(observedcollaboration, partition)
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/C0105med_train.tsv");


// Partition 0 is train data, loading test data to Partition 1

Partition truthPart = new Partition(1);

insert = data.getInserter(observedcollaboration, truthPart)
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/C0105med_test.tsv");

Database traindb = data.getDatabase(partition, [Directed, Observedcollaboration, Block, Gender, Genre, Language, Produced, Directed, Dead, ActorProdcompany, Actordistcompany, Actorquality] as Set);
Database truthdb= data.getDatabase(truthPart, [Observedcollaboration] as Set);

LazyMaxLikelihoodMPE weightLearning = new LazyMaxLikelihoodMPE(m, traindb, truthdb, config);
weightLearning.learn();
weightLearning.close();


println "\t\tLEARNING WEIGHTS DONE";

println m



//loading full data at Partition 2 and doing the inference with the learned weights
// this can also be done in a separate execution to ease the burden of the memory
 
def final_partition = new Partition(2);

insert = data.getInserter(directed, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/DA20012005med.tsv");


/*
 * Of course, we can also load data directly from tab delimited data files.
 */

insert = data.getInserter(observedcollaboration, final_partition)
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/C0105med.tsv");



insert = data.getInserter(directed, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/DA20012005med.tsv");

insert = data.getInserter(produced, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/PA20012005med.tsv");

insert = data.getInserter(genre, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AG20012005med.tsv");

insert = data.getInserter(language, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AL20012005med.tsv");

insert = data.getInserter(dead, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/Dead20012005med.tsv");

insert = data.getInserter(gender, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/Gender20012005med.tsv");

insert = data.getInserter(actorprodcompany, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AP20012005med.tsv");

insert = data.getInserter(actordistcompany, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AD20012005med.tsv");

insert = data.getInserter(actorquality, final_partition);
dir = 'data'+java.io.File.separator+'dataset_full'+java.io.File.separator;
InserterUtils.loadDelimitedData(insert, dir+"med/AQ20012005med.tsv");


Database db = data.getDatabase(final_partition, [Directed, Observedcollaboration, Block, Gender, Genre, Language, Produced, Directed, Dead, ActorProdcompany, Actordistcompany, Actorquality] as Set);
LazyMPEInference inferenceApp = new LazyMPEInference(m, db, config);
inferenceApp.mpeInference();
inferenceApp.close();



List<String> valid_data = new ArrayList<String>();

println "Inference results with hand-defined weights:"
for (GroundAtom atom : Queries.getAllAtoms(db, Collaboration))
{
//	total_count+=1;
	println atom.toString() + "\t" + atom.getValue();
//	if(atom.getValue()!=1.0)
//	{
//		valid_count +=1;
		valid_data.add(atom.toString() + "\t" + atom.getValue());
//	}
	
}


//Write results to an output tsv file, our Python script will use that file along with the test set to obtain the AUC score
writer = new BufferedWriter(new FileWriter(dir+"output.csv"));
for(int i = 0;i < valid_data.size();i++){
	writer.write(valid_data[i]);
	writer.newLine();
	}

writer.close();

/*
 * Let's see the results
 */
println "Inference results with hand-defined weights:"
for (GroundAtom atom : Queries.getAllAtoms(db, Collaboration))
	println atom.toString() + "\t" + atom.getValue();


/* We close the Databases to flush writes */
db.close();
;


