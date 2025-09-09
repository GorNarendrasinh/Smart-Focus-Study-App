function updateDateTime(){
  const now = new Date();
  const hours = now.getHours();
  const greeting = document.getElementById('greeting');
  let greetText = "Hello, Bapu!";
  if(hours < 12) greetText = "Good Morning, Bapu!";
  else if(hours < 18) greetText = "Good Afternoon, Bapu!";
  else greetText = "Good Evening, Bapu!";
  greeting.innerText = greetText;

  const dateTime = document.getElementById('dateTime');
  dateTime.innerText = now.toLocaleString();
}
setInterval(updateDateTime,1000);

// ===== Motivational Quotes =====
const quotes = [
  "Focus on your goal. Don’t look anywhere but ahead.",
  "Small steps every day lead to big results.",
  "Discipline is the bridge between goals and accomplishment.",
  "Stay focused and never give up.",
  "Your mind is a powerful tool, use it wisely."
];
function randomQuote(){
  const q = quotes[Math.floor(Math.random()*quotes.length)];
  document.getElementById('motivationalQuote').innerText = q;
}
setInterval(randomQuote,10000);




// ===== Dark Mode Toggle =====
const darkBtn = document.getElementById('darkModeBtn');
darkBtn.addEventListener('click',()=>{
  document.body.classList.toggle('dark');
});

  // ------------------ Stats Chart ------------------
  const ctx = document.getElementById('focusChart').getContext('2d');
  const focusChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'],
      datasets: [{
        label: 'Hours Focused',
        data: [2,4,3,5,6,4,3],
        backgroundColor: 'rgba(76, 175, 80, 0.7)'
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });


let goalInterval;
let pausedTime = 0;

// --- Study Planner ---
function startGoal(){
  clearInterval(goalInterval);

  let goal = document.getElementById("goalText").value;
  let durationInput = document.getElementById("goalTime").value;

  if(!goal || !durationInput){
    alert("Enter goal and time");
    return;
  }

  let parts = durationInput.split(":");
  let totalSeconds = parseInt(parts[0])*3600 + parseInt(parts[1])*60;

  // Save goal in localStorage
  let startTime = Date.now() - pausedTime*1000; // resume from paused
  localStorage.setItem("todayGoal", JSON.stringify({
    goal: goal,
    duration: totalSeconds,
    start: startTime
  }));

  updateTimer();
}

function stopGoal(){
  clearInterval(goalInterval);
  let stored = JSON.parse(localStorage.getItem("todayGoal"));
  if(stored){
    let elapsed = Math.floor((Date.now() - stored.start)/1000);
    pausedTime = elapsed;
    document.getElementById("goalTimer").innerText = formatTime(stored.duration - elapsed);
  }
}

function clearGoal(){
  clearInterval(goalInterval);
  pausedTime = 0;
  localStorage.removeItem("todayGoal");
  document.getElementById("goalTimer").innerText = "00:00:00";
  document.getElementById("goalProgress").style.width = "0%";
  document.getElementById("goalText").value = "";
  document.getElementById("goalTime").value = "";
}

// Timer update function
function updateTimer(){
  goalInterval = setInterval(()=>{
    let stored = JSON.parse(localStorage.getItem("todayGoal"));
    if(!stored) return;

    let elapsed = Math.floor((Date.now() - stored.start)/1000);
    let remaining = stored.duration - elapsed;
    let progress = (elapsed/stored.duration)*100;
    if(progress>100) progress=100;
    document.getElementById("goalProgress").style.width = progress + "%";

    if(remaining <=0){
      clearInterval(goalInterval);
      document.getElementById("goalTimer").innerText = "⏰ Time Over!";
      document.getElementById("goalProgress").style.width="100%";
      alert(`Goal "${stored.goal}" time over!`);
      document.getElementById("alarmSound").play();
      localStorage.removeItem("todayGoal");
      pausedTime = 0;
    } else {
      document.getElementById("goalTimer").innerText = formatTime(remaining);
    }
  },1000);
}

// Helper function to format seconds to HH:MM:SS
function formatTime(seconds){
  let h = Math.floor(seconds/3600);
  let m = Math.floor((seconds%3600)/60);
  let s = seconds%60;
  return `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
}

// Restore goal on page load
window.onload = function(){
  let stored = JSON.parse(localStorage.getItem("todayGoal"));
  if(stored){
    document.getElementById("goalText").value = stored.goal;
    updateTimer();
  }
}
// Load saved notes on page load
window.addEventListener('load', () => {
    const saved = JSON.parse(localStorage.getItem('savedNotes')) || [];
    saved.forEach(note => addNoteToDOM(note));
});

// Save a new note
function saveNote() {
    const noteText = document.getElementById('quickNotes').value.trim();
    if(!noteText) return alert('Please write something!');

    const saved = JSON.parse(localStorage.getItem('savedNotes')) || [];
    saved.push(noteText);
    localStorage.setItem('savedNotes', JSON.stringify(saved));

    addNoteToDOM(noteText);
    document.getElementById('quickNotes').value = '';
}

// Clear all notes
function clearNotes() {
    if(confirm('Are you sure you want to delete all notes?')) {
        localStorage.removeItem('savedNotes');
        document.getElementById('savedNotes').innerHTML = '';
    }
}

// Helper: add note to DOM
function addNoteToDOM(noteText) {
    const noteDiv = document.createElement('div');
    noteDiv.classList.add('note-item');
    noteDiv.textContent = noteText;
    document.getElementById('savedNotes').appendChild(noteDiv);
}
  // Pomodoro Timer variables
let pomodoroDuration = 25 * 60; // 25 minutes in seconds
let pomodoroTimer;
let timeLeft = pomodoroDuration;

// Start Pomodoro function
function startPomodoro() {
    clearInterval(pomodoroTimer); // stop any existing timer
    timeLeft = pomodoroDuration;
    updatePomodoroDisplay();
    pomodoroTimer = setInterval(() => {
        timeLeft--;
        updatePomodoroDisplay();
        if(timeLeft <= 0){
            clearInterval(pomodoroTimer);
            alert("Pomodoro Completed! Take a break 😊");
        }
    }, 1000);
}

// Update display
function updatePomodoroDisplay() {
    let minutes = Math.floor(timeLeft / 60);
    let seconds = timeLeft % 60;
    const display = document.getElementById('pomodoroDisplay');
    if(!display) {
        // If display div doesn't exist, create it
        const div = document.createElement('div');
        div.id = 'pomodoroDisplay';
        div.style.marginTop = '10px';
        div.style.fontSize = '1.2em';
        document.querySelector('.card').appendChild(div);
        div.textContent = `${minutes.toString().padStart(2,'0')}:${seconds.toString().padStart(2,'0')}`;
    } else {
        display.textContent = `${minutes.toString().padStart(2,'0')}:${seconds.toString().padStart(2,'0')}`;
    }
}
const input = document.getElementById('dailyInput');
const counter = document.getElementById('charCounter');
const savedDiv = document.getElementById('savedChallenge');

// Character counter
input.addEventListener('input', () => {
    counter.textContent = `${input.value.length} / 200`;
});

// Load saved challenge on page load
window.onload = function() {
    const saved = localStorage.getItem('dailyChallenge');
    if(saved) {
        savedDiv.textContent = saved;
        savedDiv.classList.add('saved');
    }
}

// Save challenge
function saveChallenge() {
    const challenge = input.value.trim();
    if(challenge === "") {
        alert("Please write a challenge!");
        return;
    }
    localStorage.setItem('dailyChallenge', challenge);
    savedDiv.textContent = challenge;
    savedDiv.classList.add('saved');
    input.value = "";
    counter.textContent = "0 / 200";

    // Brief glow effect
    savedDiv.style.background = "#fff3cd"; // yellow glow
    setTimeout(() => {
        savedDiv.style.background = "#d4edda"; // back to light green
    }, 500);
}

// Clear challenge
function clearChallenge() {
    localStorage.removeItem('dailyChallenge');
    savedDiv.textContent = "";
    savedDiv.classList.remove('saved');
}
