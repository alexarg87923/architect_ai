import React, { useEffect, useState } from "react";
import { LuPanelLeftClose } from "react-icons/lu";
import { FiTrash2 } from "react-icons/fi";
import ReactDOM from "react-dom";

export const EditNodeSidebar = ({ node, isOpen, onClose, onDelete, onUpdate }) => {
  const [title, setTitle] = useState(node?.title || "");
  const [comments, setComments] = useState(node?.comments || node?.description || "");
  const [acceptanceCriteria, setAcceptanceCriteria] = useState(node?.acceptance_criteria || []);

  useEffect(() => {
    if (node) {
      setTitle(node.title);
      setComments(node.comments ?? node.description ?? "");
      setAcceptanceCriteria(node.acceptance_criteria || []);
    }
  }, [node]);

  if (!isOpen || !node) return null;

  const handleSave = () => {
    const cleanedCriteria = (acceptanceCriteria || []).map(c => (c ?? "").trim()).filter(c => c.length > 0);
    onUpdate(node.id, { title, comments, acceptance_criteria: cleanedCriteria });
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
              Comments
            </label>
            <textarea
              value={comments}
              onChange={(e) => setComments(e.target.value)}
              rows={5}
              className="w-full px-3 py-2 rounded-md border border-gray-300 dark:border-[#3C3C3C] bg-transparent text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 outline-none resize-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-600 dark:text-gray-300 mb-2">
              Acceptance Criteria
            </label>
            <div className="space-y-2">
              {(acceptanceCriteria || []).length === 0 && (
                <div className="text-sm text-gray-500 dark:text-gray-400">No acceptance criteria yet.</div>
              )}
              {(acceptanceCriteria || []).map((crit, idx) => (
                <div key={idx} className="flex items-center gap-2">
                  <input
                    type="text"
                    value={crit}
                    onChange={(e) => {
                      const next = [...acceptanceCriteria];
                      next[idx] = e.target.value;
                      setAcceptanceCriteria(next);
                    }}
                    className="flex-1 px-3 py-2 rounded-md border border-gray-300 dark:border-[#3C3C3C] bg-transparent text-gray-900 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 outline-none"
                    placeholder={`Criterion ${idx + 1}`}
                  />
                  <button
                    type="button"
                    onClick={() => setAcceptanceCriteria(acceptanceCriteria.filter((_, i) => i !== idx))}
                    className="px-2 py-2 text-sm text-red-600 hover:bg-red-50 dark:hover:bg-[#3A3A3A] rounded-md"
                    title="Remove criterion"
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                type="button"
                onClick={() => setAcceptanceCriteria([...(acceptanceCriteria || []), ""])}
                className="px-3 py-2 text-sm text-blue-600 hover:bg-blue-50 dark:hover:bg-[#3A3A3A] rounded-md"
              >
                + Add Criterion
              </button>
            </div>
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
