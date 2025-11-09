import React, { useCallback, useMemo, useEffect } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  MiniMap,
  useNodesState,
  useEdgesState,
  addEdge,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { RoadmapNode } from './nodes/RoadmapNode';
import { StartNode } from './nodes/StartNode';

const nodeTypes = { roadmap: RoadmapNode, start: StartNode};


export const Canvas = ({ hasProject, projectName, roadmapNodes = [], onNodesChange: onRoadmapNodesChange }) => {
    
  
  const initialNodes = useMemo(() => {

    const startNodeLabel = `Get Started with - ${projectName || 'Your Project'}`;
    return [
        {
            id: 'start-node',
            type: 'start',
            position: { x: 0, y: 100 },
            data: { label: startNodeLabel },
            deletable: false,
        }
    ];

    // *** Need to add logic for adding roadmap nodes ***

  }, [hasProject, projectName, roadmapNodes]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Update nodes when initialNodes changes
  useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div className="flex-1 h-full bg-gray-50">
      <ReactFlow
        panOnScroll
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        fitViewOptions={{
          padding: 0.2,
          maxZoom: 1.2,
          minZoom: 0.1
        }}
        className="bg-gray-50"
        defaultViewport={{ x: 350, y: 0, zoom: 0.8 }} // Offset to center the StartNode horizontally
      >
        <Background />
        {/* <Controls className="bg-gray-50 border border-gray-200 rounded-lg" /> */}
        {/* <MiniMap 
          className="bg-white border border-gray-200 rounded-lg shadow-sm"
          maskColor="rgba(0, 0, 0, 0.1)"
        /> */}
      </ReactFlow>
    </div>
  );
};
