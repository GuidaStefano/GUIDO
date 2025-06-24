import React, { useState, useEffect } from 'react';
import '../ChatbotPage.css';
import '../CommunityInspector.css';
import { MdArrowBack } from 'react-icons/md';
import { Link } from "react-router-dom";

const CommunityRequests = () => {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    const jobId = sessionStorage.getItem("job_id");

    if (!jobId) {
      console.error("No job_id found in sessionStorage");
      return;
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

        const req = [
          {
            author: data.results.author,
            repository: data.results.repository
          }
        ];

        setRequests(req);
        

      } catch (err) {
        console.error("Error fetching data:", err);
      }
    };

    fetchData();

  }, []);

  return (
    <div className="country-selector-page page">
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

      {requests.length === 0 && <p>No requests found.</p>}
        <div className='vertical-div'>
          {requests.map((req, index) => (
              <Link className='voceMenu'
                key={index} to={`/request-detail?author=${encodeURIComponent(req.author)}&repository=${encodeURIComponent(req.repository)}`}
              >
                <div className='flex-col'>
                  <div>
                    <svg height="50" aria-hidden="true" viewBox="0 0 24 24" version="1.1" width="50" data-view-component="true" class="octicon octicon-mark-github v-align-middle">
                        <path d="M12 1C5.923 1 1 5.923 1 12c0 4.867 3.149 8.979 7.521 10.436.55.096.756-.233.756-.522 0-.262-.013-1.128-.013-2.049-2.764.509-3.479-.674-3.699-1.292-.124-.317-.66-1.293-1.127-1.554-.385-.207-.936-.715-.014-.729.866-.014 1.485.797 1.691 1.128.99 1.663 2.571 1.196 3.204.907.096-.715.385-1.196.701-1.471-2.448-.275-5.005-1.224-5.005-5.432 0-1.196.426-2.186 1.128-2.956-.111-.275-.496-1.402.11-2.915 0 0 .921-.288 3.024 1.128a10.193 10.193 0 0 1 2.75-.371c.936 0 1.871.123 2.75.371 2.104-1.43 3.025-1.128 3.025-1.128.605 1.513.221 2.64.111 2.915.701.77 1.127 1.747 1.127 2.956 0 4.222-2.571 5.157-5.019 5.432.399.344.743 1.004.743 2.035 0 1.471-.014 2.654-.014 3.025 0 .289.206.632.756.522C19.851 20.979 23 16.854 23 12c0-6.077-4.922-11-11-11Z"></path>
                    </svg>
                  </div>
                  <div>
                    Author: <label>{req.author}</label>
                  </div>
                  <div>
                    Repository: <label>{req.repository}</label>
                  </div>
                </div>
              </Link>
        ))}
        </div>
      </div>
    </div>
  );
};

export default CommunityRequests;
