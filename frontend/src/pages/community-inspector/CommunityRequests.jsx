import React, { useState, useEffect, useRef } from 'react';
import '../ChatbotPage.css';
import '../CommunityInspector.css';
import { MdArrowBack, MdDynamicForm, MdViewList } from 'react-icons/md';
import { Link } from "react-router-dom";

const CommunityRequests = () => {
  const [requests, setRequests] = useState([]);
  const [showNotJobId, setShowNotJobId] = useState(false);
  const intervalRef = useRef(null);

   useEffect(() => {
      const jobId = sessionStorage.getItem("job_id");

      if (!jobId) {
        setShowNotJobId(true);
        return;
      } else {
        setShowNotJobId(false);
      }

      const fetchData = async () => {
        try {
          const response = await fetch("http://localhost:5005/resolve_intent", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ job_id: jobId })
          });

          const data = await response.json();

          

          if ((data.status === "PENDING" || data.status === "STARTED") && intervalRef.current === null) {
            intervalRef.current = setInterval(fetchData, 10000);
            const req = [{
              status: data.status,
              author: data.author,
              repository: data.repository,
              startDate: data.start_date,
              endDate: data.end_date
            }];
            setRequests(req);
          }

          if (data.status === "SUCCESS") {
            const req = [{
              author: data.author,
              repository: data.repository,
              status: data.status,
              startDate: data.start_date,
              endDate: data.end_date
            }];
            setRequests(req);
            clearInterval(intervalRef.current);
            intervalRef.current = null;
            sessionStorage.setItem("is_insert_locked", false);
          }

          if (data.status === "FAILED") {
            const req = [{
              author: data.author,
              repository: data.repository,
              status: data.status,
              startDate: data.start_date,
              endDate: data.end_date,
              error: data.error
            }];
            setRequests(req);
            clearInterval(intervalRef.current);
            intervalRef.current = null;
            sessionStorage.setItem("is_insert_locked", false);
          }

        } catch (err) {
          console.error("Error fetching data:", err);
        }
      };

      fetchData();

      return () => {
        if (intervalRef.current !== null) {
          clearInterval(intervalRef.current);
          intervalRef.current = null;
        }
      };
    }, []);


  return (
    <div className="community-inspector-page page">
      <div class="chatbot-header">Powered By TOAD</div>
      <div className="header-country">
        <h2>Your Requests</h2>      
      <div>
        <Link to={"/community-inspector"} className="voceMenuText">
          <div className="voceMenu floating-back" id="4">
            <MdArrowBack className="iconaMenu" />
            <span>Go back</span>
          </div>
        </Link>
      </div>
      {!showNotJobId &&
        <div className='vertical-div'>
          {!showNotJobId &&
            <div className='vertical-div'>
              {requests.map((req, index) => {
                if (req.status === "SUCCESS") {
                  return (
                    <Link
                      className='voceMenu success-answer'
                      key={index}
                      to={`/request-detail?author=${encodeURIComponent(req.author)}&repository=${encodeURIComponent(req.repository)}`}
                    >
                      <div className='flex-col'>
                        <div>
                          <svg height="50" aria-hidden="true" viewBox="0 0 24 24" version="1.1" width="50" data-view-component="true" class="octicon octicon-mark-github v-align-middle">
                              <path d="M12 1C5.923 1 1 5.923 1 12c0 4.867 3.149 8.979 7.521 10.436.55.096.756-.233.756-.522 0-.262-.013-1.128-.013-2.049-2.764.509-3.479-.674-3.699-1.292-.124-.317-.66-1.293-1.127-1.554-.385-.207-.936-.715-.014-.729.866-.014 1.485.797 1.691 1.128.99 1.663 2.571 1.196 3.204.907.096-.715.385-1.196.701-1.471-2.448-.275-5.005-1.224-5.005-5.432 0-1.196.426-2.186 1.128-2.956-.111-.275-.496-1.402.11-2.915 0 0 .921-.288 3.024 1.128a10.193 10.193 0 0 1 2.75-.371c.936 0 1.871.123 2.75.371 2.104-1.43 3.025-1.128 3.025-1.128.605 1.513.221 2.64.111 2.915.701.77 1.127 1.747 1.127 2.956 0 4.222-2.571 5.157-5.019 5.432.399.344.743 1.004.743 2.035 0 1.471-.014 2.654-.014 3.025 0 .289.206.632.756.522C19.851 20.979 23 16.854 23 12c0-6.077-4.922-11-11-11Z"></path>
                          </svg>
                        </div>
                        <div>Author: <label>{req.author}</label></div>
                        <div>Repository: <label>{req.repository}</label></div>
                        <div>Start date: <label>{req.startDate}</label></div>
                        <div>End date: <label>{req.endDate}</label></div>
                        <div>Status: <label style={{ color: "green", marginTop: "10px" }}>{req.status}</label></div>
                      </div>
                    </Link>
                  );
                } else if (req.status === "FAILED") {
                  return (
                    <div key={index} className='voceMenu error failed-answer'>
                      <div className='flex-col'>
                        <div>
                          <svg className="error" height="50" aria-hidden="true" viewBox="0 0 24 24" version="1.1" width="50" data-view-component="true" class="octicon octicon-mark-github v-align-middle">
                              <path d="M12 1C5.923 1 1 5.923 1 12c0 4.867 3.149 8.979 7.521 10.436.55.096.756-.233.756-.522 0-.262-.013-1.128-.013-2.049-2.764.509-3.479-.674-3.699-1.292-.124-.317-.66-1.293-1.127-1.554-.385-.207-.936-.715-.014-.729.866-.014 1.485.797 1.691 1.128.99 1.663 2.571 1.196 3.204.907.096-.715.385-1.196.701-1.471-2.448-.275-5.005-1.224-5.005-5.432 0-1.196.426-2.186 1.128-2.956-.111-.275-.496-1.402.11-2.915 0 0 .921-.288 3.024 1.128a10.193 10.193 0 0 1 2.75-.371c.936 0 1.871.123 2.75.371 2.104-1.43 3.025-1.128 3.025-1.128.605 1.513.221 2.64.111 2.915.701.77 1.127 1.747 1.127 2.956 0 4.222-2.571 5.157-5.019 5.432.399.344.743 1.004.743 2.035 0 1.471-.014 2.654-.014 3.025 0 .289.206.632.756.522C19.851 20.979 23 16.854 23 12c0-6.077-4.922-11-11-11Z"></path>
                          </svg>
                        </div>
                        <div>Author: <label>{req.author}</label></div>
                        <div>Repository: <label>{req.repository}</label></div>
                        <div>Status: <label>{req.status}</label></div>
                        <div>Start date: <label>{req.startDate}</label></div>
                        <div>End date: <label>{req.endDate}</label></div>
                        <div className = "specific-error" style={{ color: "red", marginTop: "15px" }}>
                          {req.error}
                        </div>
                      </div>
                    </div>
                  );
                } else {
                  return (
                    
                    <div key={index} className='voceMenu loading'>
                      
                      <div className='flex-col'>
                        <div>
                          <svg className = "pending" height="50" aria-hidden="true" viewBox="0 0 24 24" version="1.1" width="50" data-view-component="true" class="octicon octicon-mark-github v-align-middle">
                              <path d="M12 1C5.923 1 1 5.923 1 12c0 4.867 3.149 8.979 7.521 10.436.55.096.756-.233.756-.522 0-.262-.013-1.128-.013-2.049-2.764.509-3.479-.674-3.699-1.292-.124-.317-.66-1.293-1.127-1.554-.385-.207-.936-.715-.014-.729.866-.014 1.485.797 1.691 1.128.99 1.663 2.571 1.196 3.204.907.096-.715.385-1.196.701-1.471-2.448-.275-5.005-1.224-5.005-5.432 0-1.196.426-2.186 1.128-2.956-.111-.275-.496-1.402.11-2.915 0 0 .921-.288 3.024 1.128a10.193 10.193 0 0 1 2.75-.371c.936 0 1.871.123 2.75.371 2.104-1.43 3.025-1.128 3.025-1.128.605 1.513.221 2.64.111 2.915.701.77 1.127 1.747 1.127 2.956 0 4.222-2.571 5.157-5.019 5.432.399.344.743 1.004.743 2.035 0 1.471-.014 2.654-.014 3.025 0 .289.206.632.756.522C19.851 20.979 23 16.854 23 12c0-6.077-4.922-11-11-11Z"></path>
                          </svg>
                        </div>
                        <div><label>Request</label></div>
                        <div>Author: <label>{req.author}</label></div>
                        <div>Repository: <label>{req.repository}</label></div>
                        <div>Start date: <label>{req.startDate}</label></div>
                        <div>End date: <label>{req.endDate}</label></div>
                        <div>
                          <div>Status: <label>{req.status}</label></div>
                          <img src="/images/loading.gif" alt="Loading..." style={{ height: "30px", marginTop: "10px" }} />
                        </div>
                      </div>
                    </div>
                  );
                }
              })}
  </div>
}

        </div>
      }

      {showNotJobId &&
        <div className='hor-div'>
          <span>No request found please click the following link to add requests</span>
          <Link to={"/community-insert-requests"} className="voceMenuText">
              <div className="voceMenu">
                <MdDynamicForm className="iconaMenu" />
                <span>Insert request</span>
              </div>
          </Link>
        </div>
      }
      </div>
    </div>
  );
};

export default CommunityRequests;
