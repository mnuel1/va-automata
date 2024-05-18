import React, { useState } from 'react';
import useMessageStore from '../store/chatStore';
import axios from 'axios'


const ChatBox = () => {
    const [inputValue, setInputValue] = useState('');
    const {getSelectedSessionId, addMessage } = useMessageStore();
    

    const handleMessageSend = async () => {
        if (inputValue.trim() !== '') {            
            
            setInputValue('');

            try {
                const response = await axios.post('http://127.0.0.1:4000/prompt', {
                    'prompt': inputValue,
                    'sessionID': getSelectedSessionId()
                })
    
                if (response.status === 200) {
                    
                    addMessage(getSelectedSessionId(), inputValue, response.data.response);
                    console.log('success');
                } 
    
            } catch (error) {
                alert(error)
            }
        }        
        
        
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter') {
            handleMessageSend();
        }
    };
    

    return (
        <div className="bg-[#212121] px-5 py-4 rounded-md flex justify-between">
            <input                 
                type="text" 
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyPress}
                className="bg-[#212121] text-white w-full border-0 outline-none"
                placeholder="Type your message here..."
                />

            <div className="rounded-lg bg-gray-200 p-1 cursor-pointer hover:bg-gray-300">
                <button onClick={handleMessageSend} className='flex justify-center items-center'>
                    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAABMUlEQVR4nO3UzypFURTH8Y90BwZKKQM8gDKRl2BoYsyMmRE3KblznoIXkIxkZGJigiFFYSYKUVxHp/bN6Xb+3XvPRPnWGuy1d7/fOWvttfnnlyns4AaHKmIMqzhHlIjbXkQHMI8DfLYJt2K7U9F+zGAXrymC3/hIrONylWISW6GuUUa8Yz+YxOvLItFRrOAsR7QV91jCWyIX9ySVWRyhWUI4wimmcZfINUPjU3kqKRyFXgwFk2Q+/sBMNksIN1FHXzBp318oqn8jR/wFc+FcPWU/7sNgkUGWyXW4Ua1efaWc2SsjnmZygpGQn8Bzxh/Gc9IRi1hHLayHcZUh/hCGsWtqOM7pT/zI9cRGwe0q/TRksZwjfqEiGhkGa1UZpJnEgzeuYhpln4Ze2MRjN3f/7/EDz12xqRgiakMAAAAASUVORK5CYII="/>
                </button>
            </div>

        </div>
    )
}


export default ChatBox