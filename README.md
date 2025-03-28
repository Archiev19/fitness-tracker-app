# fitness-tracker-app
<h1>🏋️‍♂️ Fitness Tracker App</h1>

<h2>📌 About</h2>
<p>The Fitness Tracker App is an interactive web-based tool designed to help users monitor their fitness journey by tracking weight, setting goals, and analyzing progress. Built using Streamlit and Firebase, it offers a seamless user experience with intuitive features, progress visualization, and multiple health dashboards.</p>

<h2>🚀 Setup Instructions</h2>
<ol>
  <li>Clone the repository</li>
  <li>Install dependencies:
    <pre>pip install -r requirements.txt</pre>
  </li>
  <li>Set up Firebase:
    <ol>
      <li>Create a new Firebase project at <a href="https://console.firebase.google.com">Firebase Console</a></li>
      <li>Enable Authentication with Email/Password</li>
      <li>Create a Firestore database</li>
      <li>Generate a service account key:
        <ol>
          <li>Go to Project Settings > Service Accounts</li>
          <li>Click "Generate New Private Key"</li>
          <li>Save the JSON file as <code>firebase-credentials.json</code> in the project root</li>
        </ol>
      </li>
    </ol>
  </li>
  <li>Run the application:
    <pre>streamlit run app2.py</pre>
  </li>
</ol>

<h2>✅ Key Features</h2>
<ul>
  <li>✔️ <b>Track Your Weight:</b> Log daily weight entries effortlessly.</li>
  <li>✔️ <b>View Weight History:</b> Check previous records in a structured table.</li>
  <li>✔️ <b>Weight Difference Calculation:</b> Automatically calculates daily weight changes.</li>
  <li>✔️ <b>Progress Graph:</b> Visualizes weight trends over time.</li>
  <li>✔️ <b>Set & Track Goal Weight:</b> Define target weight with estimated time to achieve it.</li>
  <li>✔️ <b>Delete Entries:</b> Remove specific weight logs or clear all data.</li>
  <li>✔️ <b>User Login System:</b> Personal accounts to store individual fitness data securely.</li>
  <li>✔️ <b>Leaderboard:</b> Displays top users based on weight loss over the past week.</li>
  <li>✔️ <b>Smooth Navigation:</b> Sign-up, login, and logout update instantly without page refresh.</li>
  <li>✔️ <b>Motivational Quotes:</b> Stay inspired with daily David Goggins quotes! 💪</li>
</ul>

<h2>📊 Dashboard Features</h2>
<h3>🛠️ <u>1. Main Fitness Dashboard</u></h3>
<ul>
  <li>✅ Displays weight history in a structured table.</li>
  <li>✅ Line graph showing weight fluctuations over time.</li>
  <li>✅ Estimated time to reach goal weight based on past progress.</li>
</ul>

<h3>🛠️ <u>2. Fat Percentage Calculator</u></h3>
<ul>
  <li>✅ Input weight, height, and body measurements to estimate fat percentage.</li>
  <li>✅ Uses scientifically backed formulas for accuracy.</li>
  <li>✅ Helps in tracking muscle gain and fat loss progress.</li>
</ul>

<h3>🛠️ <u>3. Health & Nutrition Dashboard</u></h3>
<ul>
  <li>✅ Calculates BMI and provides health insights.</li>
  <li>✅ Displays recommended calorie intake based on fitness goals.</li>
  <li>✅ Guides users on nutrition and fitness recommendations.</li>
</ul>

<h3>🛠️ <u>4. Running & Performance Dashboard</u></h3>
<ul>
  <li>✅ Logs running sessions with distance and pace.</li>
  <li>✅ Displays average heart rate trends over runs.</li>
  <li>✅ Compares performance improvements over time.</li>
</ul>

<h2>🔒 Security</h2>
<ul>
  <li>Secure user authentication with Firebase Auth</li>
  <li>Data stored in Firebase Firestore</li>
  <li>Protected user data and sessions</li>
  <li>Secure API endpoints</li>
</ul>

<h2>🚀 Deployment</h2>
<p>The application can be deployed to Firebase Hosting:</p>
<ol>
  <li>Install Firebase CLI:
    <pre>npm install -g firebase-tools</pre>
  </li>
  <li>Login to Firebase:
    <pre>firebase login</pre>
  </li>
  <li>Initialize Firebase:
    <pre>firebase init</pre>
  </li>
  <li>Deploy the application:
    <pre>firebase deploy</pre>
  </li>
</ol>

<h2>📖 How to Use</h2>
<ol>
  <li>🔹 <b>Sign Up/Login:</b> Create an account or log in.</li>
  <li>🔹 <b>Add Weight Entries:</b> Enter daily weight to track progress.</li>
  <li>🔹 <b>View Progress:</b> Analyze trends via table and graph.</li>
  <li>🔹 <b>Set a Goal Weight:</b> Define and estimate goal achievement time.</li>
  <li>🔹 <b>Use Dashboards:</b> Access fat percentage, running, and health insights.</li>
  <li>🔹 <b>Delete Entries:</b> Remove incorrect or unwanted data.</li>
</ol>

<h2>🚀 Future Updates</h2>
<ul>
  <li>📌 More fitness tracking features (calorie intake, workout tracking).</li>
  <li>📌 Dark mode for better readability.</li>
  <li>📌 Mobile-friendly version.</li>
</ul>

<p><b>Start your fitness journey today! 🏃‍♂️🔥</b></p>

