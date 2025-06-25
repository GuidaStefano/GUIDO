import React, { useState, useRef, useEffect } from 'react';
import '../ChatbotPage.css';
import '../CommunityInspector.css';
import { Link, useNavigate } from "react-router-dom";
import CommunityGraph from '../../components/CommunityGraph';
import { MdArrowBack, MdDynamicForm, MdViewList } from 'react-icons/md';

const RequestDetail = () => {
  const fgRef = useRef();
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [metrics, setMetrics] = useState({});
  const [patterns, setPatterns] = useState([]);
  const [members, setMembers] = useState([]);
  const [showMetrics, setShowMetrics] = useState(false);
  const [showSmells, setShowSmells] = useState(false);
  const [showMembers, setShowMembers] = useState(false);
  const [author, setAuthor] = useState();
  const [repository, setRepository] = useState();
  const [showNotJobId, setShowNotJobId] = useState(false);


  useEffect(() => {
    const jobId = sessionStorage.getItem("job_id");

    if (!jobId) {
      setShowNotJobId(true)
      return;
    } else {
      setShowNotJobId(false)
    }

    const fetchData = async () => {
      try {
        const response = await fetch("http://localhost:5005/resolve_intent", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ job_id: jobId })
        });

        const data = await response.json();

        console.log(data)

        setAuthor(data.results.author)
        
        setRepository(data.results.repository)

        if(data.status == "SUCCESS") {
          setGraphData({
            nodes: data.results.graph.nodes.map(id => ({ id })),
            links: data.results.graph.edges
          });

          setMembers(data.results.graph.nodes)


          setMetrics(data.results.metrics)

          setPatterns(data.results.patterns)
        }

      } catch (err) {
        console.error("Error fetching data:", err);
      }
    };

    fetchData();

  }, []);

  return (
    <div className="community-inspector-page page">      
        <div className=''>
          <Link to={"/community-inspector"} className="voceMenuText">
              <div className="voceMenu floating-back" id="4">
                <MdArrowBack className="iconaMenu" />
                <span>Go back</span>
              </div>
          </Link>
          <div className="voceMenu floating-back members-button" id="5" onClick={() => {setShowMembers(!showMembers); setShowSmells(false); setShowMetrics(false);}}>
            <span>Members</span>
          </div>
          <div className="voceMenu floating-back metrics-button" id="5" onClick={() => {setShowMetrics(!showMetrics); setShowSmells(false); setShowMembers(false);}}>
            <span>Metrics</span>
          </div>
          <div className="voceMenu floating-back smells-button" id="6" onClick={() => {setShowSmells(!showSmells);setShowMetrics(false); setShowMembers(false);}}>
            <span>Smells</span>
          </div>
        </div>
        <CommunityGraph graphData={graphData} />
        {!showNotJobId &&
          <div className="voceMenu floating-back author-button">
            <div>Author: {author}</div>
            <div>Repository: {repository}</div>
          </div>
        }

        {!showNotJobId &&
          <div className="voceMenu floating-back author-button">
            <div>Author: {author}</div>
            <div>Repository: {repository}</div>
          </div>
        }

      {showNotJobId &&
        <Link to={"/community-insert-requests"} className="voceMenuText">
            <div className="voceMenu">
              <MdDynamicForm className="iconaMenu" />
              <span>Insert request</span>
            </div>
        </Link>
      }
        
    
      {showMetrics && (
        <div className="overlay">
          <table className="transparent-table">
            <thead>
              <tr><th>Metric</th><th>Value</th></tr>
            </thead>
            <tbody>
              {Object.entries(metrics).map(([key, value]) => (
                typeof value === 'object' ? Object.entries(value).map(([k, v]) => (
                  <tr key={`${key}-${k}`}>
                    <td>{key}.{k}</td>
                    <td>{String(v)}</td>
                  </tr>
                )) : (
                  <tr key={key}>
                    <td>{key}</td>
                    <td>{String(value)}</td>
                  </tr>
                )
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showSmells && (
        <div className="overlay">
          <table className="transparent-table">
            <thead>
              <tr><th>Pattern</th><th>Description</th><th>Detected</th></tr>
            </thead>
            <tbody>
              {patterns.map((pattern, index) => (
                <tr key={index}>
                  <td>{pattern.name}</td>
                  <td>{pattern.description}</td>
                  <td>{pattern.detected ? 'Yes' : 'No'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {showMembers && (
        <div className="overlay">
          <table className="transparent-table">
            <thead>
              <tr>
                <th>Member GitName</th>
                <th>GitHub Link</th>
              </tr>
            </thead>
            <tbody>
              {members.map((name) => (
                <tr key={name}>
                  <td>{name}</td>
                  <td>
                    <a
                      href={`https://github.com/${name}`}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      https://github.com/{name}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

    </div>
  );
};


export default RequestDetail;
