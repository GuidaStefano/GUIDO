import React, { useState } from 'react';
import { MdArrowBack } from 'react-icons/md';
import { Link } from "react-router-dom";
import 'bootstrap/dist/css/bootstrap.min.css';


const CommunityInsertRequest = () => {
  const [request, setRequest] = useState({ repoUrl: '', endDate: '' });
  const [error, setError] = useState();
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

  const handleInputChange = (field, value) => {
    setRequest(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleReset = () => {
    setRequest({ repoUrl: '', endDate: '' });
    setError();
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    let valid = true;
    let newError = { repoUrl: '', endDate: '' };

    if (!validateRepoUrl(request.repoUrl)) {
      newError.repoUrl = 'Please enter a valid GitHub repository URL (https://github.com/username/repo)';
      valid = false;
    }

    if (!validateEndDate(request.endDate)) {
      newError.endDate = 'The date must be today or a date in the past';
      valid = false;
    }

    setError(newError);

    if (valid) {
      const parts = request.repoUrl.replace("https://github.com/", "").split("/");
      const output = {
        
          author: parts[0].replace(/[^a-zA-Z0-9_\.]/g, "_").toLowerCase(),
          repository: parts[1],
          end_date: request.endDate
        
      };

      try {
        const response = await fetch("http://localhost:5005/resolve_intent", {//replace localhost
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(output)
        });

        const data = await response.json();

        if (data.job_id && data.job_id.length == 0) {
          setModalMsg("Error processing the request.");
          setModalSubMsg("Retry later");
        } else {
          setModalMsg("Request sent successfully!");
          setModalSubMsg("Check the result in previous area");
          sessionStorage.setItem("job_id", data.job_id);
          sessionStorage.setItem("is_insert_locked", true);
        }

      } catch (err) {
        setModalMsg("Error sending the request.");
        setModalSubMsg("Retry later");
      } finally {
        setShowModal(true);
      }
    }
  };

  return (
    <div className="community-inspector-page page">
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
        <div className="div-input">
          <div className="input-div" style={{ marginBottom: '10px' }}>
            <input
              type='text'
              placeholder='https://github.com/username/repo'
              value={request.repoUrl}
              onChange={(e) => handleInputChange('repoUrl', e.target.value)}
            />
            {error && error.repoUrl &&
              <div style={{ color: 'red', fontSize: '0.9em' }}>{error.repoUrl}</div>
            }

            <input
              type='date'
              value={request.endDate}
              onChange={(e) => handleInputChange('endDate', e.target.value)}
            />
            {error && error.endDate &&
              <div style={{ color: 'red', fontSize: '0.9em' }}>{error.endDate}</div>
            }
          </div>
        </div>

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
                <button type="button" className="btn-primary" onClick={() => window.location.href = "/community-inspector"}>OK</button>
              </div>
            </div>
          </div>
        </div>
      }

    </div>
  );
};

export default CommunityInsertRequest;
