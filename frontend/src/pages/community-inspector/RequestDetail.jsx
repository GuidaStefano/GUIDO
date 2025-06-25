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
  const [showMetrics, setShowMetrics] = useState(false);
  const [showSmells, setShowSmells] = useState(false);
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

        const data = {
          "job_id": "04cf0926-1443-47f9-ba50-e66f80a73ef2",
          "results": {
            "author": "daniele_rossi",
            "graph": {
              "edges": [
                {
                  "source": "david-durrleman",
                  "target": "anders9ustafsson",
                  "weight": 1
                },
                {
                  "source": "david-durrleman",
                  "target": "alice-martin",
                  "weight": 2
                },
                {
                  "source": "anders9ustafsson",
                  "target": "cesarsouza",
                  "weight": 3
                },
                {
                  "source": "alice-martin",
                  "target": "bob-smith",
                  "weight": 1
                },
                {
                  "source": "carla-ruiz",
                  "target": "david-durrleman",
                  "weight": 2
                },
                {
                  "source": "deepak-sharma",
                  "target": "carla-ruiz",
                  "weight": 2
                },
                {
                  "source": "elena-fischer",
                  "target": "alice-martin",
                  "weight": 1
                },
                {
                  "source": "fabio-garcia",
                  "target": "gina-lee",
                  "weight": 1
                },
                {
                  "source": "gina-lee",
                  "target": "haruto-yamada",
                  "weight": 3
                },
                {
                  "source": "haruto-yamada",
                  "target": "ivan-petrov",
                  "weight": 2
                },
                {
                  "source": "bob-smith",
                  "target": "fabio-garcia",
                  "weight": 1
                },
                {
                  "source": "deepak-sharma",
                  "target": "elena-fischer",
                  "weight": 1
                },
                {
                  "source": "ivan-petrov",
                  "target": "carla-ruiz",
                  "weight": 2
                }
              ],
              "nodes": [
                "david-durrleman",
                "anders9ustafsson",
                "cesarsouza",
                "alice-martin",
                "bob-smith",
                "carla-ruiz",
                "deepak-sharma",
                "elena-fischer",
                "fabio-garcia",
                "gina-lee",
                "haruto-yamada",
                "ivan-petrov"
              ]
            },
            "metrics": {
              "dispersion": {
                "avg_geo_distance": 3433.8892193812785,
                "cultural_distance_variance": 22.621716233057025,
                "geo_distance_variance": 11354570.939798128
              },
              "engagement": {
                "m_active": 1,
                "m_comment_per_pr": 0,
                "m_stargazers": 0,
                "m_watchers": 0,
                "mm_comment_dist": 1,
                "mm_commit_dist": 0,
                "mm_filecollab_dist": 2
              },
              "formality": {
                "lifetime": 6274,
                "m_membership_type": 1.9166666666666667,
                "milestones": 36
              },
              "longevity": 77.8,
              "structure": {
                "follow_connections": true,
                "pr_connections": true,
                "repo_connections": true
              }
            },
            "patterns": [
              {
                "description": "Usually sets of people part of an organization, with a common interest, often closely dependent on their practice. Informal interactions, usually across unbound distances.",
                "detected": true,
                "name": "Informal Community (IC)"
              },
              {
                "description": "Groups of people sharing a concern, a set of problems, or a passion about a topic, who deepen their knowledge and expertise in this area by interacting frequently in the same geolocation.",
                "detected": false,
                "name": "Community of Practice (CoP)"
              },
              {
                "description": "Members are rigorously selected and prescribed by management (often in the form of FG), directed according to corporate strategy and mission.",
                "detected": true,
                "name": "Formal Network (FN)"
              },
              {
                "description": "SNs can be seen as a supertype for all OSSs. To identify an SN, it is sufficient to split the structure of organizational patterns into macrostructure and microstructure.",
                "detected": true,
                "name": "Social Network (SN)"
              },
              {
                "description": "Looser networks of ties between individuals that happen to come in contact in the same context. Their driving force is the strength of the ties between members.",
                "detected": false,
                "name": "Informal Network (IN)"
              },
              {
                "description": "A networked system of communication and collaboration connecting CoPs. Anyone can join. They span geographical and time distances alike.",
                "detected": true,
                "name": "Network of Practice (NoP)"
              },
              {
                "description": "People grouped by corporations to act on (or by means of) them. Each group has an organizational goal, called mission. Compared to FN, no reliance on networking technologies, local in nature.",
                "detected": false,
                "name": "Formal Group (FG)"
              },
              {
                "description": "People with complementary skills who work together to achieve a common purpose for which they are accountable. Enforced by their organization and follow specific strategies or organizational guidelines.",
                "detected": true,
                "name": "Project Team (PT)"
              }
            ],
            "repository": "toad-wrapper"
          },
          "status": "SUCCESS"
        }

        setGraphData({
          nodes: data.results.graph.nodes.map(id => ({ id })),
          links: data.results.graph.edges
        });

        setMetrics(data.results.metrics)

        setPatterns(data.results.patterns)

        setAuthor(data.results.author)
        
        setRepository(data.results.repository)

      } catch (err) {
        console.error("Error fetching data:", err);
      }
    };

    fetchData();

  }, []);

  return (
    <div className="country-selector-page page">      
        <div className=''>
          <Link to={"/community-inspector"} className="voceMenuText">
              <div className="voceMenu floating-back" id="4">
                <MdArrowBack className="iconaMenu" />
                <span>Go back</span>
              </div>
          </Link>
          <div className="voceMenu floating-back metrics-button" id="5" onClick={() => {setShowMetrics(!showMetrics); setShowSmells(false)}}>
            <span>Metrics</span>
          </div>
          <div className="voceMenu floating-back smells-button" id="6" onClick={() => {setShowSmells(!showSmells);setShowMetrics(false)}}>
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
    </div>
  );
};


export default RequestDetail;
