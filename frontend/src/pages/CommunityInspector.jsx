import React, { useState, useRef, useEffect } from 'react';
import './ChatbotPage.css';
import './CommunityInspector.css';
import { MdChat, MdDynamicForm, MdViewList } from 'react-icons/md';
import { Link, useNavigate } from "react-router-dom";
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js';

const CommunityInspector = () => {
  const insertRef = useRef();
  const [isLocked, setIsLocked] = useState(false);

  useEffect(() => {
    const locked = sessionStorage.getItem('is_insert_locked') == 'true';
    setIsLocked(locked);

    if (locked && insertRef.current) {
      new bootstrap.Tooltip(insertRef.current);
    }
  }, []);

  return (
    <div className="community-inspector-page page">
      <div className="chatbot-header">Powered By TOAD</div>
      <div className="header-country">
        <h2>Community Inspector</h2>
      </div>

      <div className='menu-inspect'>
        {/* Link disabilitato se isLocked */}
        <span
          ref={insertRef}
          data-bs-toggle={isLocked ? "tooltip" : undefined}
          data-bs-placement="top"
          title={isLocked ? "Another request is processing" : ""}
        >
          <Link
            to={isLocked ? "#" : "/community-insert-requests"}
            className={`voceMenuText ${isLocked ? 'disabled-link' : ''}`}
            onClick={(e) => {
              if (isLocked) e.preventDefault();
            }}
          >
            <div className="voceMenu insert-req">
              <MdDynamicForm className="iconaMenu" />
              <span>Insert request</span>
            </div>
          </Link>
        </span>

        <Link to={"/community-requests"} className="voceMenuText">
          <div className="voceMenu">
            <MdViewList className="iconaMenu" />
            <span>View your requests</span>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default CommunityInspector;
