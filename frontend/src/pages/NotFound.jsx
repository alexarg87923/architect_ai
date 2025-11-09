import { HiOutlineExclamationTriangle } from 'react-icons/hi2';

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-full text-center">
      <div className="max-w-md mx-auto">
        {/* Icon */}
        <div className="flex justify-center mb-6">
          <div className="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center">
            <HiOutlineExclamationTriangle className="w-10 h-10 text-gray-400" />
          </div>
        </div>

        {/* 404 Text */}
        <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
        
        {/* Description */}
        <h2 className="text-2xl font-semibold text-gray-700 mb-2">Page Not Found</h2>
      </div>
    </div>
  );
};

export default NotFound;
