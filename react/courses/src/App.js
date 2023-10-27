
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const flask_url = process.env.REACT_APP_FLASK_URL;

function App() {
    const [courses, setCourses] = useState([]);
    const [title, setTitle] = useState('');
    const [summary, setSummary] = useState('');

    useEffect(() => {
        // Fetch courses when component mounts
        axios.get(`${flask_url}/courses`)
            .then(response => {
                setCourses(response.data.courses);
            })
            .catch(error => {
                console.error("There was an error fetching courses!", error);
            });
    }, []);

    const addCourse = () => {
    axios.post(`${flask_url}/courses`, { title, summary })
        .then(response => {
            // Update course list
            const newCourse = response.data.course;

            setCourses([...courses, newCourse]);
            setTitle('');
            setSummary('');
        })
        .catch(error => {
            console.error("There was an error adding the course!", error);
        });
}

    const handleDelete = (courseId) => {
        axios.delete(`${flask_url}/courses/${courseId}`)
            .then(response => {
                // Update course list after successful deletion
                setCourses(prevCourses => prevCourses.filter(course => course.id !== courseId));
            })
            .catch(error => {
                console.error("There was an error deleting the course!", error);
          });
    }

const upvoteCourse = (courseId) => {
    axios.post(`${flask_url}/courses/${courseId}/upvote`)
        .then(response => {
            const updatedCourses = courses.map(course => {
                if (course.id === courseId) {
                    return {
                        ...course,
                        votes: course.votes + 1
                    };
                }
                return course;
            });

            setCourses(updatedCourses);
        })
        .catch(error => {
            console.error("There was an error upvoting the course!", error);
        });
};


    return (
        <div className="App">
            <h1>Courses App</h1>
            
            <div>
                <h2>Add Course</h2>
                <input 
                    value={title} 
                    onChange={(e) => setTitle(e.target.value)} 
                    placeholder="Title" 
                />
                <input 
                    value={summary} 
                    onChange={(e) => setSummary(e.target.value)} 
                    placeholder="Summary" 
                />
                <button onClick={addCourse}>Add Course</button>
            </div>

            <div>
                <h2>Available Courses</h2>
                <ul>
                        {courses.map(course => (
            <li key={course.id}>  {/* Use course.id as key */}
                {course.title} ({course.votes}) - {course.summary}
                <button onClick={() => handleDelete(course.id)}>Delete</button>
                <button onClick={() => upvoteCourse(course.id)}>Upvote</button>
            </li>
        ))}
	    </ul>
            </div>
        </div>
    );
}

export default App;

