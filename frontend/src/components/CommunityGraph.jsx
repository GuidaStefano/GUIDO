import React, { useRef, useEffect } from 'react';
import ForceGraph3D from 'react-force-graph-3d';

const graphData = {
  nodes: [
    { id: "david-durrleman" },
    { id: "anders9ustafsson" },
    { id: "cesarsouza" }
  ],
  links: [
    { source: "david-durrleman", target: "anders9ustafsson", weight: 1 }
  ]
};

const CommunityGraph = () => {
  const fgRef = useRef();

 

  return (
    <div style={{ width: '98%', height: '100%', maxHeight: "85vh" }}>
      <ForceGraph3D
        ref={fgRef}
        graphData={graphData}
        backgroundColor="#ffffff"
        nodeColor={() => "#00979B"}
        linkColor={() => "#000000"}
        linkWidth={link => link.weight || 1}
        nodeLabel="id"
      />
    </div>
  );
};

export default CommunityGraph;
