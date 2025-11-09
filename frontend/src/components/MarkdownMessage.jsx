import ReactMarkdown from 'react-markdown';

const MarkdownMessage = ({ content, isUserMessage }) => {
  const baseClasses = isUserMessage
    ? 'text-white'
    : 'text-gray-800 dark:text-gray-200';

  return (
    <div className={`${baseClasses} max-w-none text-sm markdown-content`}>
      <ReactMarkdown
        components={{
          // Paragraphs
          p: ({ node, ...props }) => <p className="mb-2 last:mb-0 leading-relaxed" {...props} />,

          // Lists
          ul: ({ node, ...props }) => <ul className="list-disc list-inside mb-2 ml-2 space-y-1" {...props} />,
          ol: ({ node, ...props }) => <ol className="list-decimal list-inside mb-2 ml-2 space-y-1" {...props} />,
          li: ({ node, ...props }) => <li className="mb-1 leading-relaxed" {...props} />,

          // Text formatting
          strong: ({ node, ...props }) => <strong className="font-bold" {...props} />,
          em: ({ node, ...props }) => <em className="italic" {...props} />,

          // Code
          code: ({ node, inline, ...props }) =>
            inline
              ? <code className="bg-gray-200 dark:bg-gray-700 px-1 py-0.5 rounded text-xs font-mono" {...props} />
              : <code className="block bg-gray-200 dark:bg-gray-700 px-3 py-2 rounded text-xs font-mono my-2 overflow-x-auto" {...props} />,

          // Quotes
          blockquote: ({ node, ...props }) => (
            <blockquote className="border-l-4 border-blue-500 pl-4 my-2 italic" {...props} />
          ),

          // Headings
          h1: ({ node, ...props }) => <h1 className="text-xl font-bold mb-2 mt-3" {...props} />,
          h2: ({ node, ...props }) => <h2 className="text-lg font-bold mb-2 mt-3" {...props} />,
          h3: ({ node, ...props }) => <h3 className="text-base font-bold mb-2 mt-2" {...props} />,

          // Line breaks
          br: ({ node, ...props }) => <br className="my-1" {...props} />,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
};

export default MarkdownMessage;
