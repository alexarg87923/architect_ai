import Sidebar from "../components/Sidebar";
import Agent from "../components/Agent";
import TaskSidebar from "../components/TaskSidebar";
import { Canvas } from "../components/Canvas";
import { useSelectedProject } from "../contexts/SelectedProjectContext";
import { useProjects } from "../hooks/useProjects";
import { useState, useEffect } from "react";

function Dashboard({ isDark, toggleTheme }) {
    const { selectedProject, updateRoadmapNodes } = useSelectedProject();
    const { updateProject } = useProjects();
    
    // Manage sidebar collapsed state
    const [isCollapsed, setIsCollapsed] = useState(() => {
        try {
            const savedState = localStorage.getItem('ai-pm-sidebar-collapsed');
            return savedState ? JSON.parse(savedState) : false;
        } catch (error) {
            console.error('Failed to load sidebar state:', error);
            return false;
        }
    });

    // Save sidebar state to localStorage whenever it changes
    useEffect(() => {
        try {
            localStorage.setItem('ai-pm-sidebar-collapsed', JSON.stringify(isCollapsed));
        } catch (error) {
            console.error('Failed to save sidebar state:', error);
        }
    }, [isCollapsed]);

    // Manage task sidebar collapsed state
    const [isTaskCollapsed, setIsTaskCollapsed] = useState(() => {
        try {
            const savedState = localStorage.getItem('task-sidebar-collapsed');
            return savedState ? JSON.parse(savedState) : true;
        } catch (error) {
            console.error('Failed to load task sidebar state:', error);
            return true;
        }
    });

    // Save task sidebar state to localStorage whenever it changes
    useEffect(() => {
        try {
            localStorage.setItem('task-sidebar-collapsed', JSON.stringify(isTaskCollapsed));
        } catch (error) {
            console.error('Failed to save task sidebar state:', error);
        }
    }, [isTaskCollapsed]);
    

    return (
        <div className='flex h-screen w-screen bg-gray-50 dark:bg-[#1a1a1a]'>
            <Sidebar isDark={isDark} toggleTheme={toggleTheme} isCollapsed={isCollapsed} setIsCollapsed={setIsCollapsed} />
            
            {/* Task Sidebar Strip/Panel */}
            <TaskSidebar 
                selectedProject={selectedProject} 
                isSidebarCollapsed={isCollapsed}
                isTaskCollapsed={isTaskCollapsed}
                setIsTaskCollapsed={setIsTaskCollapsed}
            />

            {/* Main content area */}
            <div className="flex-1 bg-gray-50 dark:bg-[#1a1a1a]">
                <Canvas
                    hasProject={!!selectedProject}
                    projectName={selectedProject?.name}
                    roadmapNodes={selectedProject?.roadmapNodes || []}
                    onNodesChange={updateRoadmapNodes}
                    isDark={isDark}
                    isCollapsed={isCollapsed}
                    isTaskCollapsed={isTaskCollapsed}
                />
            </div>
            {/* Floating AI Agent Chatbot */}
            <Agent />
        </div>
    )
}

export default Dashboard;