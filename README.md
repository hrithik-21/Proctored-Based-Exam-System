# Proctored-Based-Exam-System
Proctored_Based_Exam_System
Problem Statement
COVID-19 pandemic has evolved the new normal by considerably effecting student’s life to a great extent. One of the major part affected is examination. A safe and secure examination system is the utmost priority in the present time so that all the students get equal opportunity and the score obtained by each student is equivalent to one’s knowledge. Though, Current examination system in India is proctored, but do not ensure a complete transparency, resulting in increase of copy cases being ignored and the essence of evaluation on fact being hindered.

1.We aim building a Proctored based Examination System which would allow fair mode of examination ensuring that no student engages into wrong doings and student gets the score which is equivalent to his/her knowledge.
2.Our aim is to improvise the examination environment to ensure a secure examination tool which teacher could control as well as trust.
3.We aim at building a tool which is secure but at the same time is easy to use and lightweight so that the performance of the tool is not compromised.



Problem Solution
Our testing tool will be built with the following features-

The Admin will have complete right to upload the questions so that questions are not leaked.

As soon as student enters his/her login credentials we will constantly match his/her photo with the face on the screen (live face detection) to ensure no malpractice and automatically notify the teacher if student has cheated or not.

The test window will automatically be switched to Fullscreen on starting the test and thus no student will be able to open new tabs.

On navigating outside the testing windows or pressing unwanted keyboard shortcuts for cheating during examination will result in the test being terminated.

Lastly, all the student passwords will be encrypted and the teacher will be able to download the result in his local storage from the admin section to avoid data manipulation and stealing.



Implementation and Application
We aim to divide the whole project into two parts- Student and Teacher.

In the teacher section we will have three tabs- Home, Contact and Download Result.

On clicking the teacher tab firstly the user authentication will open up wherein an otp will be generated for user authentication. On successful authentication the teacher will be directed to a registration page. In case the teacher is already registered he can directly sign in from there after which the home screen will open up.


In the home screen the teacher has to follow three simple steps-
1.Firstly, the teacher has to upload the students details who will appear for the examination. This file should be in a .CSV format containing student roll no , name and the date of examination.
2.Then, teacher has to upload the images of the students giving examination. The image file name should be student roll no. This will help in automating the task of face detection as our algorithm will match the image with the face of student giving examination.
3.Lastly, the teacher has to upload a .JS file containing question number, correct answer and the options to the given question. This file will be fetched directly in the student side foe displaying questions.
4.The teacher section will also have a Contact tab in case they are stuck at some point and require assistance.
5.The final tab of teacher section will be download result wherein once the students have submitted the test the teacher would be able to see the student roll number, his/her corresponding marks and the status whether he has cheated during examination or not.

In the student section the student first needs to sign in to start the examination.
1.Once the student signs in to his/her account the webcam with in built face detection will automatically be turned on and as and when the student clicks on the start test button the window will be converted to fullscreen.
2.Once into fullscreen mode the student will have a list of instructions flashed which the student needs to read carefully.
3.Once in fullscreen mode, all the hotkey shortcuts which are used for malpractices are disabled like right click, Ctrl+all keys, Alt+tab and also the Esc key.
4. During the examination a timer would be set in which the time duration of examination will be tracked and questions will be fetched from the .JS file uploaded by the teacher
5.Once the student has finished the examination, he/she will submit the test after which their result will automatically get calculated along with the status whether they copied or not.



Tech Stack

1.HTML

2.JavaScript

3.CSS

4.Python

5.Open-CV

6.MongoDb

7.Flask
