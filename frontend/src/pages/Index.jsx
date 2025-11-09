import Sidebar from "../components/Sidebar";
import Agent from "../components/Agent";
import { Canvas } from "../components/Canvas";
import { useSelectedProject } from "../contexts/ProjectContext";

function Index() {
    const { selectedProject } = useSelectedProject();

    return (
        <div className='flex h-screen w-screen'>
            <Sidebar />
            {/* Main content area */}
            <div className="flex-1 bg-gray-50 p-6">
                <Canvas 
                    hasProject={!!selectedProject} 
                    projectName={selectedProject?.name}
                    roadmapNodes={selectedProject?.roadmapNodes || []}
                />
            </div>
            {/* Floating AI Agent Chatbot */}
            <Agent />
        </div>
    )
}

export default Index;