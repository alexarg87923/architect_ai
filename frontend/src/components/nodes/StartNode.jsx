import { Handle, Position } from '@xyflow/react';
import { LuRocket } from "react-icons/lu";

export const StartNode = ({ data }) => {
  
  return (
    <div className="bg-blue-100/20 dark:bg-blue-900/20 border-2 border-dashed border-blue-300 dark:border-blue-700 rounded-xl p-8 text-center min-w-[450px] max-w-[450px] shadow-sm hover:shadow-md transition-shadow">
      <div className="flex flex-col items-center gap-4">
        <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
          <LuRocket className="w-8 h-8 text-white" />
        </div>
        <h3 className="text-xl font-semibold text-gray-900 dark:text-white">{data.label}</h3>
        <p className="text-gray-500 dark:text-[#9f9f9f] leading-relaxed">
          Get started by describing your project to me. I'll help you create a detailed roadmap and make sure you achieve your goals!
        </p>
      </div>
      
      <Handle
        type="source"
        position={Position.Bottom}
      />
    </div>
  );
};