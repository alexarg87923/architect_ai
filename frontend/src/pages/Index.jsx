import Sidebar from "../components/Sidebar";
import Agent from "../components/Agent";
import { Canvas } from "../components/Canvas";
import { useProjects } from "../hooks/useProjects";

function Index() {
    const { currentProject } = useProjects();

    return (
        <div className='flex h-screen w-screen'>
            <Sidebar />
            {/* Main content area */}
            <div className="flex-1 bg-gray-50 p-6">
                <Canvas 
                    hasProject={!!currentProject} 
                    projectName={currentProject?.name}
                    roadmapNodes={currentProject?.roadmapNodes || []}
                />
            </div>
            {/* Floating AI Agent Chatbot */}
            <Agent />
        </div>
    )
}

export default Index;