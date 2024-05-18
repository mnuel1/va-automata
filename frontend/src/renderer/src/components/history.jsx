import useMessageStore from '../store/chatStore';
import logo from '../assets/logo_no_text.png'

const ChatHistory = () => {
    const { sessions, getSelectedSessionId} = useMessageStore();    
    const selectedSession = sessions[getSelectedSessionId()];

    console.log("selectedSession:", selectedSession);

    return(
        <>
            <div className='max-h-[500px] xl:max-h-[900px] overflow-y-auto mt-6'>

            
                {selectedSession.map((message, index) => (
                    <div key={index} className='flex flex-col gap-8 p-4'>
                        <div className='mt-6 text-right'>
                            <span className='w-fit text-white bg-[#212121] p-4 rounded-md'>
                                {message.message}
                            </span>
                        </div>
                        <div className='flex '>
                            
                            <img src={logo} alt="" className='mt-2 w-12 h-5'/>
                            
                            <span className='w-fit text-white bg-[#212121] p-4 rounded-md'>
                                {message.response}
                            </span>
                        </div>
                    </div>
                    
                ))}
            </div>
            </>
    )
}

export default ChatHistory