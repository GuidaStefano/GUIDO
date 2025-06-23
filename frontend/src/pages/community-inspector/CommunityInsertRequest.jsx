import React, { useState } from 'react';
import { MdArrowBack } from 'react-icons/md';
import { Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';

const CommunityInsertRequest = () => {
  const [requests, setRequests] = useState([
    { repoUrl: '', endDate: '' }
  ]);
  const [errors, setErrors] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [modalMsg, setModalMsg] = useState('');
  const [modalSubMsg, setModalSubMsg] = useState('');


  const validateRepoUrl = (url) => {
    const regex = /^https:\/\/github\.com\/[^/]+\/[^/]+\/?$/;
    return regex.test(url);
  };

  const validateEndDate = (date) => {
    const selectedDate = new Date(date);
    const today = new Date();
    selectedDate.setHours(0, 0, 0, 0);
    today.setHours(0, 0, 0, 0);
    return selectedDate <= today;
  };

  const handleInputChange = (index, field, value) => {
    const updatedRequests = [...requests];
    updatedRequests[index][field] = value;
    setRequests(updatedRequests);
  };

  const handleAddBlock = () => {
    setRequests([...requests, { repoUrl: '', endDate: '' }]);
    setErrors([...errors, { repoUrl: '', endDate: '' }]);
  };

  const handleRemoveBlock = (index) => {
    console.log("remove")
    const updatedRequests = requests.filter((_, i) => i !== index);
    const updatedErrors = errors.filter((_, i) => i !== index);

    setRequests(updatedRequests);
    setErrors(updatedErrors);
  };

  const handleReset = () => {
    setRequests([{ repoUrl: '', endDate: '' }]);
    setErrors([]);
  };
 const handleSubmit = async (e) => {
    e.preventDefault();

    let valid = true;
    const newErrors = requests.map((req) => {
      let error = { repoUrl: '', endDate: '' };
      if (!validateRepoUrl(req.repoUrl)) {
        error.repoUrl = 'Please enter a valid GitHub repository URL (https://github.com/username/repo)';
        valid = false;
      }
      if (!validateEndDate(req.endDate)) {
        error.endDate = 'The date must be today or a date in the past';
        valid = false;
      }
      return error;
    });

    setErrors(newErrors);

    if (valid) {
      const output = {
        requests: requests.map((req) => {
          const parts = req.repoUrl.replace("https://github.com/", "").split("/");
          return {
            author: parts[0].replace(/[^a-zA-Z0-9_\.]/g, "_").toLowerCase(),
            repository: parts[1],
            end_date: req.endDate
          };
        })
      };

      try {
        const response = await fetch('https://toadmock.free.beeceptor.com/insertRequest', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(output)
        });

        const data = await response.json();
        
        if (data.exceptions.length > 0) {
          
          setModalMsg("Error processing the request.");
          setModalSubMsg("Retry later")
        } else {
          setModalMsg("Request sent successfully!");
          setModalSubMsg("Check the result in previous area")
        }

      } catch (err) {
        console.log("data")
        setModalMsg("Error sending the request.");
        setModalSubMsg("Retry later")
      } finally {
        setShowModal(true);
      }
    }
  };

  return (
    <div className="country-selector-page page">
      <div className="chatbot-header">Powered By TOAD</div>
      <div className="header-country">
        <h2>Insert Request</h2>
      </div>

      <div className='menu-inspect'>
        <Link to={"/community-inspector"} className="voceMenuText">
          <div className="voceMenu floating-back" id="4">
            <MdArrowBack className="iconaMenu" />
            <span>Go back</span>
          </div>
        </Link>
      </div>

      <form className='form-request' onSubmit={handleSubmit}>
        {requests.map((req, index) => (
          <div className="div-input">
            <div key={index} className = "input-div" style={{ marginBottom: '10px'}}>
              <input
                type='text'
                placeholder='https://github.com/username/repo'
                value={req.repoUrl}
                onChange={(e) => handleInputChange(index, 'repoUrl', e.target.value)}
              />
              {errors[index] && errors[index].repoUrl &&
                <div style={{ color: 'red', fontSize: '0.9em' }}>{errors[index].repoUrl}</div>
              }

              <input
                type='date'
                value={req.endDate}
                onChange={(e) => handleInputChange(index, 'endDate', e.target.value)}
              />
              {errors[index] && errors[index].endDate &&
                <div style={{ color: 'red', fontSize: '0.9em' }}>{errors[index].endDate}</div>
              }
            </div>
            <div className='vertical-buttons'>         
              <button className="btn-primary" type="button" onClick={handleAddBlock}>+</button>
              {index > 0 &&
                  <button className="btn-primary" type="button" onClick={() => handleRemoveBlock(index)} >
                    -
                  </button>
              }

            </div>
          </div>

        ))}

        <div className='horizontal-buttons'>
          <button className="btn-primary" type="submit">Submit</button>
          <button className="btn-primary" type="button" onClick={handleReset}>Reset</button>
        </div>
      </form>

      {showModal &&
        <div className="modal show d-block" tabIndex="-1">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="modal-header">
                <h5 className="modal-title">{modalMsg}</h5>
                <button type="button" className="btn-close" onClick={() => setShowModal(false)}></button>
              </div>
              <div className="modal-body">
                <p>{modalSubMsg}</p>
              </div>
              <div className="modal-footer">
                <button type="button" className="btn-primary" onClick={() => setShowModal(false)}>OK</button>
              </div>
            </div>
          </div>
        </div>
      }

    </div>
  );
};

export default CommunityInsertRequest;
