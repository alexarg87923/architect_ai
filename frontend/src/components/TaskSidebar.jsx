import React, { useState, useEffect } from 'react';
import { FaChevronLeft, FaChevronRight, FaLightbulb } from 'react-icons/fa';
import { PiCoffeeFill } from "react-icons/pi";
import SmartTabItemModal from './modals/SmartTabItemModal';
import TaskSection from './TaskSection';

const TaskSidebar = ({ selectedProject, isSidebarCollapsed }) => {
    const [isTaskCollapsed, setIsTaskCollapsed] = useState(() => {
        try {
            const savedState = localStorage.getItem('task-sidebar-collapsed');
            return savedState ? JSON.parse(savedState) : true;
        } catch (error) {
            console.error('Failed to load task sidebar state:', error);
            return true;
        }
    });

    useEffect(() => {
        try {
            localStorage.setItem('task-sidebar-collapsed', JSON.stringify(isTaskCollapsed));
        } catch (error) {
            console.error('Failed to save task sidebar state:', error);
        }
    }, [isTaskCollapsed]);

    // Mock tasks data -- NEED to be replaced with actual data fetching logic
    const [tasks, setTasks] = useState({
         "daily-todos": [
            { id: 1, text: "Catch up with Joseph", completed: false },
            { id: 2, text: "Watch documentary", completed: false },
            { id: 3, text: "Fix the room lighting", completed: false },
            { id: 4, text: "Provide feedback on Emily's designs", completed: false },
            { id: 5, text: "Buy new sweatshirts", completed: false },
        ],
        "your-ideas": [
            { id: 6, text: "Read 20 pages", completed: false },
            { id: 7, text: "Buy a gift from the mall for friend", completed: false },
            { id: 8, text: "Ask landlord about rent", completed: false },
            { id: 9, text: "Design 2024 family calendar", completed: false },
        ]
    });

    const [contextMenu, setContextMenu] = useState({ show: false, x: 0, y: 0, task: null, sectionKey: null });
    const [editingTaskId, setEditingTaskId] = useState(null);
    const [editingText, setEditingText] = useState("");
    const [editingSectionKey, setEditingSectionKey] = useState(null);

    const cancelRename = () => {
        setEditingTaskId(null);
        setEditingText("");
        setEditingSectionKey(null);
    };

    const saveRename = (sectionKey, task) => {
        setTasks(prev => ({
            ...prev,
            [sectionKey]: prev[sectionKey].map(t => t.id === task.id ? { ...t, text: editingText } : t)
        }));
        cancelRename();
    };

    const closeContextMenu = () => setContextMenu({ show: false, x: 0, y: 0, task: null, sectionKey: null });

    const handleRename = (sectionKey, task) => {
        requestAnimationFrame(() => {
            setEditingTaskId(task.id);
            setEditingText(task.text);
            setEditingSectionKey(sectionKey);
        });
        closeContextMenu();
    };

    const handleDelete = (sectionKey, task) => {
        setTasks(prev => ({
            ...prev,
            [sectionKey]: prev[sectionKey].filter(t => t.id !== task.id)
        }));
        closeContextMenu();
    };

    return (
        <div className="relative">
            {/* Collapsed Strip */}
            {isTaskCollapsed && (
                isSidebarCollapsed ? (
                    <div 
                        onClick={() => setIsTaskCollapsed(false)}
                        className="fixed top-20 left-0 z-40 rounded-r-lg shadow-lg bg-white dark:bg-[#232324] hover:bg-gray-50 dark:hover:bg-[#3A3A3A] border-r border-b border-t border-gray-200 dark:border-[#3C3C3C] w-5 h-[80vh] transition-colors flex items-center justify-center"
                    >
                        <FaChevronRight className="w-4 h-4 text-gray-400" />
                    </div>
                ) : (
                    <div
                        onClick={() => setIsTaskCollapsed(false)}
                        className="w-5 h-full bg-white dark:bg-[#2a2a2a] border-r border-gray-200 dark:border-[#3C3C3C] cursor-pointer hover:bg-gray-50 dark:hover:bg-[#3A3A3A] transition-colors flex items-center justify-center"
                    >
                        <FaChevronRight className="w-4 h-4 text-gray-400" />
                    </div>
                )
            )}

            {/* Expanded Panel */}
            {!isTaskCollapsed && (
                isSidebarCollapsed ? (
                    <>
                        {/* Overlay for mobile */}
                        <div
                            className="fixed top-20 left-0 inset-0 bg-black bg-opacity-50 z-20 md:hidden"
                            onClick={() => setIsTaskCollapsed(true)}
                        />
                        
                        {/* Task Panel */}
                        <div className="fixed top-20 left-0 z-40 w-80 h-[80vh] rounded-r-lg bg-white dark:bg-[#2a2a2a] border-r border-b border-t border-gray-200 dark:border-[#3C3C3C] overflow-y-auto">
                            {/* Header */}
                            <div className="flex items-center justify-between px-4 py-2 border-b border-gray-200 dark:border-[#3C3C3C]">
                                <div className="flex items-center p-2 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-[#3C3C3C] text-xs text-blue-600 dark:text-blue-300">
                                    Define your own project-specific tasks
                                </div>
                                <button
                                    onClick={() => setIsTaskCollapsed(true)}
                                    className="p-1 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] rounded transition-colors"
                                >
                                    <FaChevronLeft className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                                </button>
                            </div>

                            {/* Content */}
                            <div className="p-4">
                                {/* Todos Section */}      
                                <TaskSection
                                    title="Today Todos"
                                    placeholderText="Add todos here"
                                    sectionKey="daily-todos"
                                    tasks={tasks["daily-todos"]}
                                    icon={PiCoffeeFill}
                                    color="gray"
                                    setTasks={setTasks}
                                    editingTaskId={editingTaskId}
                                    editingText={editingText}
                                    editingSectionKey={editingSectionKey}
                                    setEditingText={setEditingText}
                                    cancelRename={cancelRename}
                                    saveRename={saveRename}
                                    setContextMenu={setContextMenu}
                                />

                                {/* Ideas Section */}
                                <TaskSection
                                    title="Your Ideas"
                                    placeholderText="Add ideas here"
                                    sectionKey="your-ideas"
                                    tasks={tasks["your-ideas"]}
                                    icon={FaLightbulb}
                                    color="gray"
                                    setTasks={setTasks}
                                    editingTaskId={editingTaskId}
                                    editingText={editingText}
                                    editingSectionKey={editingSectionKey}
                                    setEditingText={setEditingText}
                                    cancelRename={cancelRename}
                                    saveRename={saveRename}
                                    setContextMenu={setContextMenu}
                                />
                            </div>
                        </div>
                    </>
                ) : (
                    <>
                        {/* Overlay for mobile */}
                        <div
                            className="fixed inset-0 bg-black bg-opacity-50 z-20 md:hidden"
                            onClick={() => setIsTaskCollapsed(true)}
                        />
                        
                        {/* Task Panel */}
                        <div className="w-80 h-full bg-white dark:bg-[#2a2a2a] border-r border-gray-200 dark:border-[#3C3C3C] overflow-y-auto">
                            {/* Header */}
                            <div className="flex items-center justify-between p-4 border-b border-gray-200 dark:border-[#3C3C3C]">
                                <div className="flex items-center space-x-2">
                                    <h2 className="font-semibold text-md text-gray-900 dark:text-white">Smart Tab</h2>
                                </div>
                                <button
                                    onClick={() => setIsTaskCollapsed(true)}
                                    className="p-1 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] rounded transition-colors"
                                >
                                    <FaChevronLeft className="w-4 h-4 text-gray-500 dark:text-gray-400" />
                                </button>
                            </div>

                            {/* Content */}
                            <div className="p-4">
                                {/* Project Header */}
                                {selectedProject && (
                                    <div className="mb-6 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-[#3C3C3C] text-xs text-blue-600 dark:text-blue-300">
                                        Define your own project-specific tasks
                                    </div>
                                )}

                                {/* Todos Section */}      
                                <TaskSection
                                    title="Today Todos"
                                    placeholderText="Add todos here"
                                    sectionKey="daily-todos"
                                    tasks={tasks["daily-todos"]}
                                    icon={PiCoffeeFill}
                                    color="gray"
                                    setTasks={setTasks}
                                    editingTaskId={editingTaskId}
                                    editingText={editingText}
                                    editingSectionKey={editingSectionKey}
                                    setEditingText={setEditingText}
                                    cancelRename={cancelRename}
                                    saveRename={saveRename}
                                    setContextMenu={setContextMenu}
                                />

                                {/* Ideas Section */}
                                <TaskSection
                                    title="Your Ideas"
                                    placeholderText="Add ideas here"
                                    sectionKey="your-ideas"
                                    tasks={tasks["your-ideas"]}
                                    icon={FaLightbulb}
                                    color="gray"
                                    setTasks={setTasks}
                                    editingTaskId={editingTaskId}
                                    editingText={editingText}
                                    editingSectionKey={editingSectionKey}
                                    setEditingText={setEditingText}
                                    cancelRename={cancelRename}
                                    saveRename={saveRename}
                                    setContextMenu={setContextMenu}
                                />
                            </div>
                        </div>
                    </>
                )
            )}
            <SmartTabItemModal
                isOpen={contextMenu.show}
                x={contextMenu.x}
                y={contextMenu.y}
                task={contextMenu.task}
                sectionKey={contextMenu.sectionKey}
                onClose={closeContextMenu}
                onRename={handleRename}
                onDelete={handleDelete}
            />
        </div>
    );
};

export default TaskSidebar;