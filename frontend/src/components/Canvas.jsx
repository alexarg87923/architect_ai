import React, { useCallback, useMemo, useEffect, useState } from 'react';
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
import { SubtaskNode } from './nodes/SubtaskNode';
import { ProjectOverviewModal } from './modals/ProjectOverviewModal';
// icon imports
import { MdFilterCenterFocus } from "react-icons/md";

const nodeTypes = { roadmap: RoadmapNode, start: StartNode, subtask: SubtaskNode };


export const Canvas = ({ hasProject, projectName, roadmapNodes = [], onNodesChange: onRoadmapNodesChange, isDark, isCollapsed, isTaskCollapsed }) => {
  
  // Modal state for project overview
  const [isOverviewModalOpen, setIsOverviewModalOpen] = useState(false);
  const [selectedNodeForOverview, setSelectedNodeForOverview] = useState(null);

  // Function to open the overview modal with selected node data
  const openOverviewModal = useCallback((nodeData) => {
    setSelectedNodeForOverview(nodeData);
    setIsOverviewModalOpen(true);
  }, []);

  // Function to close the overview modal
  const closeOverviewModal = useCallback(() => {
    setIsOverviewModalOpen(false);
    setSelectedNodeForOverview(null);
  }, []);
  
  // Handle subtask completion toggle
  const handleSubtaskToggle = useCallback((parentNodeId, subtaskId, completed) => {
    // Update the roadmap nodes with the new subtask completion status
    const updatedNodes = roadmapNodes.map(node => {
      if (node.id === parentNodeId || `roadmap-${roadmapNodes.indexOf(node)}` === parentNodeId) {
        const updatedSubtasks = node.subtasks.map(subtask => 
          subtask.id === subtaskId ? { ...subtask, completed } : subtask
        );
        
        // Calculate completion percentage for the parent node
        const completedSubtasks = updatedSubtasks.filter(st => st.completed).length;
        const completion_percentage = Math.round((completedSubtasks / updatedSubtasks.length) * 100);
        
        // Update parent node status based on completion
        let status = 'pending';
        if (completion_percentage === 100) {
          status = 'completed';
        } else if (completion_percentage > 0) {
          status = 'in-progress';
        }
        
        return {
          ...node,
          subtasks: updatedSubtasks,
          completion_percentage,
          status
        };
      }
      return node;
    });
    
    // Notify parent component of the changes
    if (onRoadmapNodesChange) {
      onRoadmapNodesChange(updatedNodes);
    }
  }, [roadmapNodes, onRoadmapNodesChange]);
    
  
  const initialNodes = useMemo(() => {
    const nodes = [];
    
    // Always include the start node
    const startNodeLabel = `Get Started with - ${projectName || 'Your Project'}`;
    nodes.push({
      id: 'start-node',
      type: 'start',
      position: { x: 0, y: 100 },
      data: { label: startNodeLabel },
      deletable: false,
    });

    // Add roadmap nodes if they exist
    if (roadmapNodes && roadmapNodes.length > 0) {
      roadmapNodes.forEach((node, index) => {
        const nodeId = node.id || `roadmap-${index}`;
        
        // Add the main roadmap node
        nodes.push({
          id: nodeId,
          type: 'roadmap',
          position: { 
            x: 0, // Keep all nodes in a single column, aligned with StartNode
            y: 530 + index * 450 // Increased gap to accommodate subtasks
          },
          data: {
            title: node.title,
            description: node.description,
            estimatedDays: node.estimated_days || node.estimatedDays,
            estimatedHours: node.estimated_hours || node.estimatedHours,
            tags: node.tags || [],
            status: node.status || 'pending',
            category: node.tags?.[0] || 'development', // Use first tag as category
            completionPercentage: node.completion_percentage || 0,
            subtasks: node.subtasks || [],
            deliverables: node.deliverables || [],
            dependencies: node.dependencies || [],
            overview: node.overview || null, // Add the overview field (will only be present for setup nodes)
            onOpenOverviewModal: openOverviewModal
          },
          deletable: false,
        });

        // Add subtask nodes for this roadmap node
        if (node.subtasks && node.subtasks.length > 0) {
          node.subtasks.forEach((subtask, subtaskIndex) => {
            const subtaskId = `${nodeId}-subtask-${subtaskIndex}`;
            
            // Determine if this roadmap node should have subtasks on left or right
            const isRightSide = index % 2 === 0; // Even index = right, odd index = left
            
            // Base X position based on side - single column for clear order
            const baseX = isRightSide ? 600 : -450; // Right side starts at 600, left side at -450

            // Calculate centered positioning around the roadmap node
            const roadmapNodeY = 530 + index * 450; // Y position of the roadmap node
            const totalSubtasks = node.subtasks.length;
            const totalHeight = (totalSubtasks - 1) * 140; // Total height needed for all subtasks
            const startY = roadmapNodeY - (totalHeight / 2) + 50; // Start position to center around roadmap node + small offset
            
            nodes.push({
              id: subtaskId,
              type: 'subtask',
              position: {
                x: baseX, // Single column, no horizontal offset
                y: startY + subtaskIndex * 140 // Center around roadmap node with clear spacing
              },
              data: {
                subtask: subtask,
                parentNodeId: nodeId,
                onToggleComplete: handleSubtaskToggle
              },
              deletable: false,
            });
          });
        }
      });
    }

    return nodes;
  }, [hasProject, projectName, roadmapNodes, handleSubtaskToggle]);

  const initialEdges = useMemo(() => {
    const edges = [];
    
    if (roadmapNodes && roadmapNodes.length > 0) {
      // Connect start node to first roadmap node
      if (roadmapNodes[0]) {
        edges.push({
          id: 'start-to-first',
          source: 'start-node',
          target: roadmapNodes[0].id || 'roadmap-0',
          type: 'smoothstep',
          animated: true,
        });
      }
      
      // Create sequential connections between roadmap nodes
      roadmapNodes.forEach((node, index) => {
        const nodeId = node.id || `roadmap-${index}`;
        
        // Connect to next roadmap node (top to bottom)
        if (index < roadmapNodes.length - 1) {
          const nextId = roadmapNodes[index + 1].id || `roadmap-${index + 1}`;
          
          edges.push({
            id: `roadmap-${index}-to-${index + 1}`,
            source: nodeId,
            sourceHandle: 'bottom',
            target: nextId,
            targetHandle: 'top',
            type: 'smoothstep',
            animated: false,
          });
        }

        // Connect roadmap node to its subtasks
        if (node.subtasks && node.subtasks.length > 0) {
          node.subtasks.forEach((subtask, subtaskIndex) => {
            const subtaskId = `${nodeId}-subtask-${subtaskIndex}`;
            
            // Determine connection side based on roadmap node index
            const isRightSide = index % 2 === 0; // Even index = right, odd index = left
            const sourceHandle = isRightSide ? 'right' : 'left';
            const targetHandle = isRightSide ? 'left' : 'right'; // Subtask connects from opposite side
            
            edges.push({
              id: `${nodeId}-to-${subtaskId}`,
              source: nodeId,
              sourceHandle: sourceHandle,
              target: subtaskId,
              targetHandle: targetHandle,
              type: 'smoothstep',
              style: { 
                stroke: '#94a3b8', 
                strokeWidth: 1.5,
                strokeOpacity: 0.6
              },
              animated: false,
            });
          });
        }
      });
    }
    
    return edges;
  }, [roadmapNodes]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // Reactive viewport that updates when sidebar state changes
  const [viewport, setViewport] = useState({ x: 400, y: 0, zoom: 0.7 });
  const centerViewport = useCallback(() => {
    let defaultViewport = isCollapsed
      ? { x: 600, y: 0, zoom: 0.7 }
      : { x: 400, y: 0, zoom: 0.7 };
    if (!isTaskCollapsed && !isCollapsed) {
      defaultViewport = { x: 300, y: 0, zoom: 0.7 };
    }
    setViewport(defaultViewport);
  }, [isCollapsed, isTaskCollapsed]);

  // Update viewport when sidebar or task sidebar state changes
  useEffect(() => {
    let defaultViewport = isCollapsed
      ? { x: 600, y: 0, zoom: 0.7 }
      : { x: 400, y: 0, zoom: 0.7 };
    if (!isTaskCollapsed && !isCollapsed) {
      defaultViewport = { x: 300, y: 0, zoom: 0.7 };
    }
    setViewport(defaultViewport);
  }, [isCollapsed, isTaskCollapsed]);

  // Update nodes and edges when initialNodes or initialEdges change
  useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  useEffect(() => {
    setEdges(initialEdges);
  }, [initialEdges, setEdges]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div className="flex-1 h-full">
      <ReactFlow
        panOnScroll
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        colorMode={isDark ? 'dark' : 'light'}
        fitViewOptions={{
          padding: 0.2,
          maxZoom: 1.2,
          minZoom: 0.1
        }}
        viewport={viewport}
        onViewportChange={setViewport} // Allow manual viewport changes
      >
        <Background />
        {/* <Controls className="bg-gray-50 border border-gray-200 rounded-lg" /> */}
        {/* <MiniMap 
          className="bg-white border border-gray-200 rounded-lg shadow-sm"
          maskColor="rgba(0, 0, 0, 0.1)"
        /> */}
      </ReactFlow>
      <button
        onClick={centerViewport}
        className="absolute top-5 right-5 bg-white dark:bg-[#2a2a2a] border border-gray-200 dark:border-[#3C3C3C] rounded-lg p-2 shadow-sm transition-all duration-200 group text-gray-400 dark:text-gray-300 hover:text-gray-600 dark:hover:text-gray-100 cursor-pointer"
      >
        <MdFilterCenterFocus className="w-6 h-6" />
      </button>

      <ProjectOverviewModal
        isOpen={isOverviewModalOpen}
        onClose={closeOverviewModal}
        nodeData={selectedNodeForOverview}
      />
    </div>
  );
};
