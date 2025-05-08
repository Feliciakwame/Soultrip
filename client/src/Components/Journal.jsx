import React, { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import "./Journal.css";

function Journal() {
  const [entries, setEntries] = useState([]);
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const { id } = useParams(); // Get user ID from URL params

  useEffect(() => {
    fetch(`http://localhost:5000/journal_entries/user/${id}`)
      .then((res) => res.json())
      .then((data) => setEntries(data))
      .catch((err) => console.error("Error fetching journal entries:", err));
  }, [id]);

  const handleSubmit = (e) => {
    e.preventDefault();

    fetch("http://localhost:5000/journal_entries", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title,
        content,
        user_id: id, // send user ID so the backend knows who the entry belongs to
      }),
    })
      .then((res) => res.json())
      .then((newEntry) => setEntries([...entries, newEntry]))
      .catch((err) => console.error("Error creating journal entry:", err));

    setTitle("");
    setContent("");
  };

  return (
    <div className="journal">
      <h2>📝 My Soul Journal</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Title of your thoughts..."
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Write your feelings, moments, or magic here..."
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        />
        <button type="submit">✨ Save Entry</button>
      </form>

      <div className="entry-list">
        {entries.map((entry) => (
          <div key={entry.id} className="entry-card">
            <h3>{entry.title}</h3>
            <p>{entry.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Journal;
