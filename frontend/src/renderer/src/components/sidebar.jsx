import React, { useState, useEffect } from 'react';
import Logo from "./logo"
import useMessageStore from '../store/chatStore';

const Sidebar = () => {    
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);
    const { sessions, selectSession } = useMessageStore()
    const mdBreakpoint = 768;

    const toggleSidebar = () => {
        setIsSidebarOpen(!isSidebarOpen);
    };

    useEffect(() => {
        const checkScreenSize = () => {
            if (window.innerWidth >= mdBreakpoint) {
                setIsSidebarOpen(false)
            }            
        };
    
        checkScreenSize();
      
        window.addEventListener('resize', checkScreenSize);
        
        return () => {
            window.removeEventListener('resize', checkScreenSize);
        };
    }, []);
   
    return (
        <>    
            <div className="md:hidden absolute w-full z-50">
                <button onClick={toggleSidebar} className={`absolute top-[20px] ${isSidebarOpen ? 'left-[240px]': 'left-[30px]'}`}>
                    <img 
                        className='w-10 h-10' 
                        src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAQ0lEQVR4nO3WoREAIAwEQfovKyksSAQimrDbwc2bXwsAOKoq6z05JSSuEAAAaD36fnNKSPQTAQDAkPebU0LiCgGAn21ViEka78Lu0AAAAABJRU5ErkJggg=="/>
                </button>
            </div>

            <div className={`flex flex-col min-w-[200px] xl:min-w-[300px] border-r border-white border-opacity-10 p-6 z-50 bg-[#121212] 
                ${isSidebarOpen ? 'flex absolute h-full' : 'hidden md:flex'}`}>
                            
                <div className="flex items-center mt-5 px-2 py-1">
                    <Logo />
                </div>
            
                <div className="flex flex-col flex-grow gap-2 mt-12">
                    <h2 className='text-white font-semibold'>History</h2>
                    <div className='max-h-[430px] lg:max-h-[800px] overflow-y-auto'>                       
                        {sessions.map((_, index) => (
                            <button 
                                key={index} 
                                className="mt-2 w-full h-[40px] bg-[#212121] text-white flex p-2 items-center rounded-md cursor-pointer
                                hover:bg-[#1E1E2E]"
                                onClick={() => selectSession(index)}>
                                Session {index + 1}
                                
                            </button>
                        ))}

                        
                        {/* <div className="mt-2 w-full h-[60px] bg-white"></div> */}
                    </div>
                                        
                </div>
                
                <div className="flex items-center justify-center">
                    <span className="text-[7px] lg:text-xs text-gray-400 opacity-40">© 2024 BSCSNS - 3AB™. All rights reserved.</span>
                </div>
            </div>
        </>
    )

}

export default Sidebar