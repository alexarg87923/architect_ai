import React, { useEffect, useState } from "react";
import { LuPanelLeftClose } from "react-icons/lu";
import { FiTrash2 } from "react-icons/fi";
import ReactDOM from "react-dom";

export const EditNodeSidebar = ({ node, isOpen, onClose, onDelete, onUpdate }) => {
  const [title, setTitle] = useState(node?.title || "");
  const [description, setDescription] = useState(node?.description || "");

  useEffect(() => {
    if (node) {
      setTitle(node.title);
      setDescription(node.description);
    }
  }, [node]);

  if (!isOpen || !node) return null;

  const handleSave = () => {
    onUpdate(node.id, { title, description });
    onClose();
  };

  const handleDelete = () => {
    onDelete(node.id);
    onClose();
  };

  return (
    ReactDOM.createPortal(
      <div className="fixed right-0 top-0 h-full w-80 bg-white dark:bg-[#2a2a2a] border-l border-gray-200 dark:border-[#3C3C3C] shadow-lg flex flex-col z-50 transition-transform duration-300">
        {/* Header */}
        <div className="p-4 flex items-center justify-between border-b border-gray-100 dark:border-[#3C3C3C]">
          <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
            Edit Node
          </h2>
          <LuPanelLeftClose
            className="w-6 h-6 text-gray-400 dark:text-gray-300 cursor-pointer hover:text-gray-600 dark:hover:text-gray-100"
            onClick={onClose}
          />
        </div>

        {/* Form Content */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">
              Title
            </label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-[#3C3C3C] bg-transparent text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-1">
              Description
            </label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={5}
              className="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-[#3C3C3C] bg-transparent text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
            />
          </div>
        </div>

        {/* Actions */}
        <div className="p-4 border-t border-gray-100 dark:border-[#3C3C3C] flex justify-between">
          <button
            onClick={handleDelete}
            className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-[#3A3A3A] rounded-md"
          >
            <FiTrash2 className="w-4 h-4" />
            Delete
          </button>

          <div className="flex gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-[#3A3A3A] rounded-md text-sm font-medium"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md text-sm font-medium"
            >
              Save
            </button>
          </div>
        </div>
      </div>,
      document.body
    )
  );
};
