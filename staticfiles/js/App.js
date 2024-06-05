import React, { useState } from 'react';
import axios from 'axios';

function App() {
    const [userChoice, setUserChoice] = useState('');
    const [result, setResult] = useState(null);

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('/api/play_prisoners_dilemma/', { user_choice: userChoice });
            setResult(response.data);
        } catch (error) {
            console.error("There was an error!", error);
        }
    };

    return (
        <div>
            <h1>Play Prisoner's Dilemma</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Your Choice:
                    <select value={userChoice} onChange={(e) => setUserChoice(e.target.value)} required>
                        <option value="">--Select--</option>
                        <option value="Cooperate">Cooperate</option>
                        <option value="Defect">Defect</option>
                    </select>
                </label>
                <button type="submit">Play</button>
            </form>
            {result && (
                <div>
                    <h2>Results</h2>
                    <p>You chose: {result.user_choice}</p>
                    <p>Opponent chose: {result.opponent_choice}</p>
                    <p>Your Score: {result.user_score}</p>
                    <p>Opponent Score: {result.opponent_score}</p>
                </div>
            )}
        </div>
    );
}

export default App;