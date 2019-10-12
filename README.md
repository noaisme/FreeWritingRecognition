# Free Writing Recognition
A memory test &amp; parser for a free writing task.
The following is a part of a research in psychology exploring dissociation and memory performance. 

## 1. Introduction
Our goal was to examine subjects’ memory regarding free text they have just written. We wanted to analyze their recognition abilities according to signal-detection theory, i.e. to generate measures of Hit, Correct rejection, Miss (omission error) and False alarm (commission error) from their answers. 

In our experiment, participants were instructed to perform free writing for several minutes (as in, whatever comes to mind with no guidelines or editing whatsoever). Afterwards, we wanted to test their memory on the just written text. Therefore, we wanted to create a custom recognition test for each participant, in which he or she will be asked to discriminate between segments of text that were written by him/herself, during free writing, and control segments of text pre-prepared by the experimenter. Importantly, **this whole experiment was administered in Hebrew**, therefore the attached code files are suitable for Hebrew and R-T-L languages. It requires minor modification in order to be used in other languages - feel free to contact us if you wish to do so, we will gladly help.
Also, the main focus for us was the experiment itself rather than code quality. On most cases making the code more robust or efficient should be rather easy, and your feedback is of course welcome.

## 2. How does it work?
<em>Note that while we decided to use segments of two words (=bigrams), the change to support any other n-gram should be easy enough.</em>


- **Before the experiment:** As a prelimineary step for the entire experiment and before any participant was enrolled, we created a pool of control bigrams, based on several pre-tests conducted among students and lab members. 
- The participant performs free writing in a text editor of your choice. it is crucial that he/she **cannot** see what is typed. This can be achieved, for example, by writing with white font over white background, and making font size extremely small. <em> Note that we excluded this step from our code, and do not cover it here.</em> The text itself is then saved by the experimenter in a text file - i.e. <code> RawInput.txt </code>.
- The parser script  (<code>FreeWritingParse.py</code>) asks the experimenter for a subject ID, and to choose the free written text file (In our example, <code> RawInput.txt </code>). It then parses it into bigrams, and randomly chooses 20 of them: 10 from the 1st half of the text and 10 from the 2nd half. The parser script is defined such that if there are bigrams in the subject's text that are identical to control bigrams, they are not selected. The selected 20 bigrams, as well as 10 control bigrams, are printed into a text file that is the output of the parser, and is named <code> PreTest_\<SubjectID\>.txt </code>. 
- Then, an experimenter <em>manually</em> scans <code> PreTest_\<SubjectID\>.txt </code>, in order to make sure the user-generated bigrams in it do not include names or spelling mistakes, which can skew the subject-performance in the recognition test. In case there are notable names or mistakes in the user-generated bigrams, these bigrams are deleted by the experimenter. In case there aren’t any names or mistakes, the experimenter randomly deletes 5 user bigrams from the 1st half of the text and 5 user bigrams from the 2nd half of the text, such that eventually <code> PreTest_\<SubjectID\>.txt </code> includes 10 user bigrams and 10 control bigrams. 
- The experimenter now runs the experiment script (<code>FreeWriting_Experiment.py</code>). Again, the script asks for the Subject ID   and for the PreTest file for this subject ID (that would be <code> PreTest_\<SubjectID\>.txt</code> ).
- The experiment starts. The subject is presented with 20 bigrams, in a random order. Each bigram is presented alongside two action buttons: "I wrote it" and "I didn't write it", which the subject has to choose from according to his/her judegement. The experiment script documents the subjects' responses and cross-checks them with the PreTest file. Thus, for each response, it is recorded whether it is correct (“True”) or incorrect (“False”), and from which part of the text the bigram was taken (1st part, 2nd part of control). In case of an incorrect identification, the script documents the type of error – a commission error or an omission error.
- Results can be seen in the generated CSV, which is named <code>MemoryTestResults_\<SubjectID\>.csv</code>.
  
We've included an example pretest, results, and controlled bigrams within the repository.
  


