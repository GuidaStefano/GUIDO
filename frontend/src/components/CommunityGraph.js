import React, { useRef } from 'react';
import ForceGraph3D from 'react-force-graph-3d';

const CommunityGraph = ({graphData}) => {
  const fgRef = useRef();
  

  return (
    <div style={{ height: '100%', maxHeight: "85vh" }}>
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
