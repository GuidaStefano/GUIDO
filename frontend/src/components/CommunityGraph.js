import { useEffect, useRef, useState } from 'react';
import ForceGraph3D from 'react-force-graph-3d';
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.min.js';


const MyGraph = ({ graphData }) => {
  const fgRef = useRef();
  const sliderRef = useRef();
  const [distance, setDistance] = useState(50);

  useEffect(() => {
    if (sliderRef.current) {
      const existingTooltip = bootstrap.Tooltip.getInstance(sliderRef.current);
      if (existingTooltip) {
        existingTooltip.dispose();
      }

      sliderRef.current.setAttribute('title', `Node Distance: ${distance}`);

      new bootstrap.Tooltip(sliderRef.current);
    }
  }, [distance]);

  useEffect(() => {
    if (sliderRef.current) {
      new bootstrap.Tooltip(sliderRef.current);
    }
  }, []);

  useEffect(() => {
    if (
      fgRef.current &&
      fgRef.current.d3Force &&
      graphData?.nodes?.length > 0 &&
      fgRef.current.d3Force('link')
    ) {
      fgRef.current.d3Force('link').distance(distance);
      fgRef.current.d3ReheatSimulation();
    }
  }, [distance, graphData]);


  return (
    <>
      <div style={{ height: '100%', maxHeight: "85vh" }}>
        <ForceGraph3D
          ref={fgRef}
          graphData={graphData}
          backgroundColor="#ffffff"
          nodeColor={() => "#00979B"}
          linkColor={() => "#000000"}
          linkWidth={link => 1}
          nodeLabel="id"
        />
      </div>
      <div style={{ padding: '10px' }}>
        <label
          className='label-distance'
        >
          <input
            ref={sliderRef}
            type="range"
            min="50"
            max="500"
            step="10"
            className='input-slide voceMenu'
            value={distance}
            onChange={(e) => setDistance(Number(e.target.value))}
            data-bs-toggle="tooltip"
            data-bs-placement="top"
            title={`Node Distance: ${distance}`}
          />
        </label>

      </div>
    </>
  );
};

export default MyGraph;
