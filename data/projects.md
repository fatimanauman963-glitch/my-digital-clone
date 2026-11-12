# My projects in detail

## QR code based secure attendance system
This was a web application I built to make attendance faster and more trustworthy. Instead of calling names in class or passing around a paper sheet, attendance is marked through QR codes. The word "secure" is important here: the goal was that attendance cannot be easily faked, for example by someone marking attendance for a friend who is not in class.
The idea is simple. A QR code is generated for a class session, students scan it, and their attendance is recorded in the system. I built it as part of my software engineering coursework at UMT.

I built it with plain HTML, CSS and JavaScript, and I ran and tested it using the Live Server extension in VS Code. The system has two sides. The teacher portal is where a teacher manages courses and sessions and generates the QR code for a class. The student portal is where a student scans the code to mark attendance. There is also course and session management, so attendance is organised per course and per class session, and a live dashboard that shows attendance as it comes in.
What I learned from this project is how to plan a system with different user roles (teacher and student), how to structure the front end so each portal stays clean, and why attendance data needs to be protected from misuse. It was a good practical application of the ideas from my Software Construction and Development course.

## Voice recorder
I also built a voice recorder application. It lets a user record their voice and save the audio. It was a smaller project than the attendance system, but it taught me how applications work with audio input.


## Smart Medicine Reminder and Compartment System (IoT)
This was a group project for my IoT course. It uses an ESP32 microcontroller to remind a person when to take their medicine, with a compartment system to organize the medicines. The idea is to help people, especially elderly ones, who forget their medicine times.
The hardware plan includes an ESP32 as the brain, a DS3231 real-time clock module to keep accurate time even when power is off, a buzzer and LEDs to alert the person, push buttons so the person can confirm they took the medicine, a reed or IR sensor to detect whether a compartment was opened, and an OLED or LCD display to show messages. All of it sits in a medicine box with separate compartments. I like this project because it solves a real everyday problem with simple, affordable parts.

## Digital clone chatbot
For my NLP-related coursework I built this chatbot. It uses retrieval-augmented generation: it searches my own notes with BM25 keyword search and sentence embeddings, combines both rankings, and then answers in first person only from what it found.
