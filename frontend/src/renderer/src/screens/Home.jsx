
import Intro from "../components/intro"
import QuickAccess from "../components/quickaccess"
import ChatBox from "../components/chats"
import useMessageStore from "../store/chatStore"
import ChatHistory from "../components/history"

const Home = () => {
    const { hasMessages, getSelectedSessionId } = useMessageStore();
    const selectedSessionId = getSelectedSessionId();
    
    return (
        <>              
            <div className="w-full flex flex-col justify-center items-center p-4 relative ">
                {hasMessages(selectedSessionId) ?
                    <div className='w-full xl:w-[900px] h-full mb-24'>
                        <ChatHistory/>
                    </div> 
                : 
                <>                                    
                    <Intro/>
                                                            
                    <div className="grid grid-cols-1 xl:grid-cols-2 mt-12 gap-2 mb-14">                        
                        <QuickAccess title={"Sample title"} description={"Sample description"}/>
                        <QuickAccess title={"Sample title"} description={"Sample description"}/>                  
                        <QuickAccess title={"Sample title"} description={"Sample description"}/>
                        <QuickAccess title={"Sample title"} description={"Sample description"}/>
                
                    </div>
                </>
                }
                

                <div className="absolute bottom-0 w-full xl:w-[900px]">
                    <ChatBox/>
                </div>
            
            </div>     
           
        
        </>
       
    )


}

export default Home