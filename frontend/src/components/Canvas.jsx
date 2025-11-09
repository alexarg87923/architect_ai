import React, { useCallback, useMemo, useEffect, useState, useRef } from 'react';
import {
  ReactFlow,
  Background,
  Controls,
  useNodesState,
  useEdgesState,
  addEdge,
  useReactFlow,
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { RoadmapNode } from './nodes/RoadmapNode';
import { StartNode } from './nodes/StartNode';
import { SubtaskNode } from './nodes/SubtaskNode';
import { ProjectOverviewModal } from './modals/ProjectOverviewModal';

// Component to handle fitView based on container dimensions
const FitViewOnChange = ({ containerRef, nodesToFitView }) => {
  const { fitView } = useReactFlow();
  const [containerDimensions, setContainerDimensions] = useState({ width: 0, height: 0 });

  const handleFitView = useCallback(() => {
    fitView({
      minZoom: 0.6,
      maxZoom: 0.6,
      duration: 100,
    });
  }, [fitView]);

  // Observe container dimension changes
  useEffect(() => {
    if (!containerRef?.current) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;
        setContainerDimensions({ width, height });
      }
    });

    resizeObserver.observe(containerRef.current);

    return () => {
      resizeObserver.disconnect();
    };
  }, [containerRef]);

  // Call fitView when container dimensions change
  useEffect(() => {
    if (containerDimensions.width > 0 && containerDimensions.height > 0) {
      const timeoutId = setTimeout(handleFitView, 100);
      return () => clearTimeout(timeoutId);
    }
  }, [handleFitView, containerDimensions]);

  return null; // This component doesn't render anything
};



export const Canvas = ({ hasProject, projectName, roadmapNodes = [], roadmapEpics = [], onNodesChange: onRoadmapNodesChange, isDark, isCollapsed, isTaskCollapsed }) => {
  const nodeTypes = { roadmap: RoadmapNode, start: StartNode, subtask: SubtaskNode };

  // Backward compatibility: use roadmapEpics if provided, otherwise roadmapNodes
  const epics = roadmapEpics.length > 0 ? roadmapEpics : roadmapNodes;

  // Container reference for responsive centering
  const containerRef = useRef(null);

  // Modal state for project overview
  const [isOverviewModalOpen, setIsOverviewModalOpen] = useState(false);
  const [selectedNodeForOverview, setSelectedNodeForOverview] = useState(null);
  // Track which subtask node is currently selected (for exclusive active state)
  const [selectedSubtaskNodeId, setSelectedSubtaskNodeId] = useState(null);

  // Function to open the overview modal with selected epic data
  const openOverviewModal = useCallback((epicData) => {
    setSelectedNodeForOverview(epicData);
    setIsOverviewModalOpen(true);
  }, []);

  // Function to close the overview modal
  const closeOverviewModal = useCallback(() => {
    setIsOverviewModalOpen(false);
    setSelectedNodeForOverview(null);
  }, []);

  // Handle story completion toggle
  const handleStoryToggle = useCallback((parentEpicId, storyId, completed) => {
    const updatedEpics = epics.map(epic => {
      const epicNodeId = String(epic.id);
      if (epicNodeId === parentEpicId) {
        const stories = epic.stories || epic.subtasks || [];
        const updatedStories = stories.map(story => {
          if (story.id === storyId) {
            return { ...story, completed };
          }
          return story;
        });

        const completedStories = updatedStories.filter(st => st.completed).length;
        const completion_percentage = Math.round((completedStories / updatedStories.length) * 100);

        let status = 'pending';
        if (completion_percentage === 100) {
          status = 'completed';
        } else if (completion_percentage > 0) {
          status = 'in-progress';
        }

        return {
          ...epic,
          stories: updatedStories,
          subtasks: updatedStories, // Backward compatibility
          completion_percentage,
          status
        };
      }
      return epic;
    });

    // Notify parent component of the changes
    if (onRoadmapNodesChange) {
      onRoadmapNodesChange(updatedEpics);
    }
  }, [epics, onRoadmapNodesChange]);

  // Handle story update (title/description/etc.)
  const handleStoryUpdate = useCallback((parentEpicId, storyId, updates) => {
    const updatedEpics = epics.map(epic => {
      const epicNodeId = String(epic.id);
      if (epicNodeId === parentEpicId) {
        const stories = epic.stories || epic.subtasks || [];
        const updatedStories = stories.map(story => {
          if (story.id === storyId) {
            return { ...story, ...updates };
          }
          return story;
        });

        const completedStories = updatedStories.filter(st => st.completed).length;
        const completion_percentage = Math.round((completedStories / updatedStories.length) * 100);

        let status = 'pending';
        if (completion_percentage === 100) {
          status = 'completed';
        } else if (completion_percentage > 0) {
          status = 'in-progress';
        }

        return {
          ...epic,
          stories: updatedStories,
          subtasks: updatedStories, // Backward compatibility
          completion_percentage,
          status
        };
      }
      return epic;
    });

    if (onRoadmapNodesChange) {
      onRoadmapNodesChange(updatedEpics);
    }
  }, [epics, onRoadmapNodesChange]);

  // Handle story delete
  const handleStoryDelete = useCallback((parentEpicId, storyId) => {
    const updatedEpics = epics.map(epic => {
      const epicNodeId = String(epic.id);
      if (epicNodeId === parentEpicId) {
        const stories = epic.stories || epic.subtasks || [];
        const updatedStories = stories.filter(story => story.id !== storyId);

        const completedStories = updatedStories.filter(st => st.completed).length;
        const completion_percentage = updatedStories.length === 0 ? 0 : Math.round((completedStories / updatedStories.length) * 100);

        let status = 'pending';
        if (completion_percentage === 100 && updatedStories.length > 0) {
          status = 'completed';
        } else if (completion_percentage > 0) {
          status = 'in-progress';
        }

        return {
          ...epic,
          stories: updatedStories,
          subtasks: updatedStories, // Backward compatibility
          completion_percentage,
          status
        };
      }
      return epic;
    });

    if (onRoadmapNodesChange) {
      onRoadmapNodesChange(updatedEpics);
    }
  }, [epics, onRoadmapNodesChange]);


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

    // Add epic nodes if they exist
    if (epics && epics.length > 0) {
      epics.forEach((epic, index) => {
        const epicId = String(epic.id);

        // Add the main epic node
        nodes.push({
          id: epicId,
          type: 'roadmap',
          position: {
            x: 0, // Keep all nodes in a single column, aligned with StartNode
            y: 530 + index * 450 // Increased gap to accommodate stories
          },
          data: {
            // New schema (epics)
            title: epic.name || epic.title, // Support both name (new) and title (old)
            description: epic.description || 'No description provided',
            estimatedDays: epic.estimated_days || epic.estimatedDays || 7, // Default to 7 days if not provided
            estimatedHours: epic.estimated_hours || epic.estimatedHours || 0,
            tags: epic.tags || [],
            status: epic.status || 'pending',
            category: epic.tags?.[0] || epic.priority || 'development', // Use first tag or priority as category
            completionPercentage: epic.completion_percentage || 0,
            subtasks: epic.stories || epic.subtasks || [], // Support both stories (new) and subtasks (old)
            deliverables: epic.deliverables || [],
            dependencies: epic.dependencies || [],
            overview: epic.overview || null,
            onOpenOverviewModal: openOverviewModal
          },
          deletable: false,
          hidden: false, // Explicitly set to not hidden
        });

        // Add story nodes for this epic
        const stories = epic.stories || epic.subtasks || [];
        if (stories && stories.length > 0) {
          stories.forEach((story, storyIndex) => {
            const storyId = `${epicId}-subtask-${storyIndex}`;

            // Determine if this epic should have stories on left or right
            const isRightSide = index % 2 === 0; // Even index = right, odd index = left

            // Base X position based on side - single column for clear order
            const baseX = isRightSide ? 600 : -450; // Right side starts at 600, left side at -450

            // Calculate centered positioning around the epic node
            const epicNodeY = 530 + index * 450; // Y position of the epic node
            const totalStories = stories.length;
            const totalHeight = (totalStories - 1) * 140; // Total height needed for all stories
            const startY = epicNodeY - (totalHeight / 2) + 50; // Start position to center around epic node + small offset

            nodes.push({
              id: storyId,
              type: 'subtask',
              position: {
                x: baseX, // Single column, no horizontal offset
                y: startY + storyIndex * 140 // Center around epic node with clear spacing
              },
              data: {
                subtask: story, // Keep name as subtask for component compatibility
                parentNodeId: epicId, // React Flow node ID (string)
                onToggleComplete: handleStoryToggle,
                onUpdate: handleStoryUpdate,
                onDelete: handleStoryDelete,
                nodeId: storyId,
                selectedNodeId: selectedSubtaskNodeId,
                setSelectedNodeId: setSelectedSubtaskNodeId
              },
              deletable: false,
            });
          });
        }
      });
    }

    return nodes;
  }, [hasProject, projectName, epics, handleStoryToggle, openOverviewModal, selectedSubtaskNodeId]);

  const initialEdges = useMemo(() => {
    const edges = [];
    console.log('🔍 Creating edges, epics count:', epics?.length || 0);

    if (epics && epics.length > 0) {
      // Connect start node to first epic
      if (epics[0]) {
        edges.push({
          id: 'start-to-first',
          source: 'start-node',
          target: String(epics[0].id || 'roadmap-0'),
          type: 'smoothstep',
          style: {
            strokeWidth: 1.5,
          },
          animated: false,
        });
      }

      // Create sequential connections between epic nodes
      epics.forEach((epic, index) => {
        const epicId = String(epic.id);

        // Connect to next epic node (top to bottom)
        if (index < epics.length - 1) {
          const nextId = String(epics[index + 1].id);

          edges.push({
            id: `roadmap-${index}-to-${index + 1}`,
            source: epicId,
            sourceHandle: 'bottom',
            target: nextId,
            targetHandle: 'top',
            type: 'smoothstep',
            style: {
              strokeWidth: 1.5,
            },
            animated: false,
          });
        }

        // Connect epic node to its stories
        const stories = epic.stories || epic.subtasks || [];
        if (stories && stories.length > 0) {
          stories.forEach((story, storyIndex) => {
            const storyId = `${epicId}-subtask-${storyIndex}`;

            // Determine connection side based on epic node index
            const isRightSide = index % 2 === 0; // Even index = right, odd index = left
            const sourceHandle = isRightSide ? 'right' : 'left';
            const targetHandle = isRightSide ? 'left' : 'right'; // Story connects from opposite side

            edges.push({
              id: `${epicId}-to-${storyId}`,
              source: epicId,
              sourceHandle: sourceHandle,
              target: storyId,
              targetHandle: targetHandle,
              type: 'smoothstep',
              style: {
                strokeWidth: 1.5,
              },
              animated: false,
            });
          });
        }
      });
    }

    console.log('✅ Created edges count:', edges.length);
    return edges;
  }, [epics]);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const nodesToFitView = nodes; // Show all nodes in viewport

  // Update nodes and edges when initialNodes or initialEdges change
  useEffect(() => {
    setNodes(initialNodes);
  }, [initialNodes, setNodes]);

  useEffect(() => {
    console.log('📊 useEffect updating edges, count:', initialEdges.length);
    console.log('📊 First few edges:', initialEdges.slice(0, 3));
    setEdges(initialEdges);
  }, [initialEdges, setEdges]);

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div ref={containerRef} className="flex-1 h-full">
      <style>{`
        .react-flow__node {
          visibility: visible !important;
        }
        .react-flow__edge {
          visibility: visible !important;
        }
      `}</style>
      <ReactFlow
        panOnScroll
        nodes={nodes}
        edges={edges}
        onInit={() => console.log('🎨 ReactFlow initialized, edges:', edges.length)}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        nodeTypes={nodeTypes}
        colorMode={isDark ? 'dark' : 'light'}
        nodesDraggable={false}
        nodesConnectable={false}
        onlyRenderVisibleElements={false}
        defaultViewport={{ x: 0, y: 0, zoom: 0.4 }}
        fitViewOptions={{
          padding: 0.2,
          maxZoom: 1.2,
          minZoom: 0.1
        }}
        // viewport={viewport}
        // onViewportChange={setViewport} // Allow manual viewport changes
      >
        <Background />
        <FitViewOnChange containerRef={containerRef} nodesToFitView={nodesToFitView} />
        <Controls showZoom={false} showInteractive={false} position="top-right" fitViewOptions={{ minZoom: 0.6, maxZoom: 0.6, duration: 100 }} className="border border-gray-200 dark:border-[#3C3C3C]" />
      </ReactFlow>

      <ProjectOverviewModal
        isOpen={isOverviewModalOpen}
        onClose={closeOverviewModal}
        nodeData={selectedNodeForOverview}
      />
    </div>
  );
};
