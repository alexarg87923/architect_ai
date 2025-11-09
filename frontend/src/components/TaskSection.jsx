import React, { useState, useEffect, useRef } from 'react';
import { FaPlus } from 'react-icons/fa';

function TaskItem({ task, onToggle, sectionKey, editingTaskId, editingText, setEditingText, cancelRename, saveRename, setContextMenu }) {
    const inputRef = useRef(null);

    useEffect(() => {
        const shouldFocus = editingTaskId === task.id;
        const isMounted = !!inputRef.current;

        if (shouldFocus && isMounted) {
            requestAnimationFrame(() => {
                if (inputRef.current) {
                    inputRef.current.focus();
                    inputRef.current.select();
                }
            });
        }
    }, [editingTaskId, task.id]);

    const handleKeyDown = (e) => {
        if (e.key === 'Enter') {
            saveRename(sectionKey, task);
        } else if (e.key === 'Escape') {
            cancelRename();
        }
    };

    return (
        <div className="py-1 border-t border-gray-200 dark:border-[#3C3C3C]">
            <div
                className="flex items-center space-x-3 px-2 py-2 hover:bg-gray-50 dark:hover:bg-[#3A3A3A] group rounded-lg"
                onContextMenu={e => {
                    e.preventDefault();
                    setContextMenu({ show: true, x: e.clientX, y: e.clientY, task, sectionKey });
                }}
            >
                <button
                    onClick={() => onToggle(task.id)}
                    className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                        task.completed
                            ? 'bg-green-500 border-green-500'
                            : 'border-gray-300 dark:border-gray-600 hover:border-green-400'
                    }`}
                >
                    {task.completed && <span className="text-white text-xs">✓</span>}
                </button>
                {editingTaskId === task.id ? (
                    <input
                        ref={inputRef}
                        type="text"
                        value={editingText}
                        onChange={e => setEditingText(e.target.value)}
                        onBlur={cancelRename}
                        onKeyDown={handleKeyDown}
                        className="flex-1 bg-transparent outline-none text-sm text-gray-900 dark:text-white border-none focus:bg-white dark:focus:bg-[#3A3A3A] px-1 w-full"
                    />
                ) : (
                    <div className={`text-sm flex-1 ${task.completed ? 'line-through text-gray-500' : 'text-gray-900 dark:text-white'}`}>
                        {task.text}
                    </div>
                )}
            </div>
        </div>
    );
}

const TaskSection = ({ title, placeholderText, sectionKey, tasks, icon: Icon, color = "blue", setTasks, editingTaskId, editingText, editingSectionKey, setEditingText, cancelRename, saveRename, setContextMenu }) => {
    const [adding, setAdding] = useState(false);
    const [input, setInput] = useState("");
    const inputRef = useRef(null);
    const addBoxRef = useRef(null);

    useEffect(() => {
        if (adding && inputRef.current) inputRef.current.focus();
    }, [adding]);

    useEffect(() => {
        if (!adding) return;
        function handleClick(e) {
            if (addBoxRef.current && !addBoxRef.current.contains(e.target)) {
                setAdding(false);
                setInput("");
            }
        }
        document.addEventListener('mousedown', handleClick);
        return () => document.removeEventListener('mousedown', handleClick);
    }, [adding]);

    const handleAdd = () => {
        if (input.trim() === "") return;

        setTasks(prev => {
            const key = sectionKey;
            const nextId = Math.max(0, ...(prev[key] || []).map(t => t.id)) + 1;
            return {
                ...prev,
                [key]: [
                    ...(prev[key] || []),
                    { id: nextId, text: input, completed: false }
                ]
            };
        });
        setInput("");
        setAdding(false);
    };

    return (
        <div className="mb-6">
            <div className={`flex items-center space-x-2 mb-3 ml-2 text-${color}-600 dark:text-${color}-400`}>
                <Icon className="w-4 h-4" />
                <h3 className="font-semibold text-sm">{title}</h3>
            </div>
            {adding ? (
                <div ref={addBoxRef} className="flex items-center space-x-2 p-2 w-full bg-gray-50 dark:bg-[#3A3A3A] rounded-lg">
                    <input
                        ref={inputRef}
                        className="flex-1 bg-transparent outline-none text-sm text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
                        placeholder="Add a new task..."
                        value={input}
                        onChange={e => setInput(e.target.value)}
                        onKeyDown={e => {
                            if (e.key === 'Enter') handleAdd();
                            if (e.key === 'Escape') { setAdding(false); setInput(""); }
                        }}
                    />
                </div>
            ) : (
                <button
                    className="flex items-center space-x-2 p-2 w-full text-left text-gray-500 dark:text-gray-400 rounded-lg bg-gray-50 dark:bg-[#3A3A3A] cursor-pointer"
                    onClick={() => setAdding(true)}
                >
                    <FaPlus className="w-3 h-3" />
                    <span className="text-sm">{placeholderText}</span>
                </button>
            )}
            <div className='pt-2'>
                {(tasks || []).map(task => (
                    <TaskItem
                        key={`${task.id}-${editingTaskId === task.id ? 'editing' : 'normal'}`}
                        task={task}
                        onToggle={(id) => {
                            setTasks(prev => ({
                                ...prev,
                                [sectionKey]: (prev[sectionKey] || []).map(t =>
                                    t.id === id ? { ...t, completed: !t.completed } : t
                                )
                            }));
                        }}
                        sectionKey={sectionKey}
                        editingTaskId={editingSectionKey === sectionKey ? editingTaskId : null}
                        editingText={editingText}
                        setEditingText={setEditingText}
                        cancelRename={cancelRename}
                        saveRename={saveRename}
                        setContextMenu={setContextMenu}
                    />
                ))}
            </div>
        </div>
    );
};

export default TaskSection;
