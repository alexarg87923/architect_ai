import { Handle, Position } from '@xyflow/react';
import { LuRocket } from "react-icons/lu";

export const StartNode = ({ data }) => {
  
  return (
    <div className="bg-white border-2 border-dashed border-gray-300 rounded-xl p-8 text-center min-w-[300px] shadow-sm hover:shadow-md transition-shadow">
      <div className="flex flex-col items-center gap-4">
        <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
          <LuRocket className="w-8 h-8 text-white" />
        </div>
        <h3 className="text-xl font-semibold text-gray-900">{data.label}</h3>
        <p className="text-gray-500 max-w-sm">
          Get started by describing your project to me. I'll help you create a detailed roadmap and make sure you achieve your goals!
        </p>
      </div>
      
      <Handle
        type="source"
        position={Position.Bottom}
        className="w-3 h-3 bg-blue-500 border-2 border-white"
      />
    </div>
  );
};