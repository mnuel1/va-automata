
import {create} from 'zustand';
import axios from 'axios';


const useMessageStore = create((set, get) => ({
    sessions: [],
    selectedSessionId: 0,
    
    init: async () => {
        try {
            const response = await axios.get('http://127.0.0.1:4000/chats');
            const sessions = response.data.chats;        
            set({ sessions });
        } catch (error) {
            console.error('Error initializing sessions:', error);
        }
    },
    
    addMessage: (sessionId, message, response) =>
        set((state) => {
            const sessionIndex = state.sessions.findIndex((_, index) => index === sessionId);
    
            if (sessionIndex !== -1) {              
                return {
                    sessions: state.sessions.map((session, index) =>
                        index === sessionIndex
                            ? [ 
                                ...session,
                                {  
                                    message: message,
                                    response: response
                                }
                            ]
                            : session
                    )
                };
            } else {              
                return {
                    sessions: [
                        ...state.sessions, 
                        [ 
                            {  
                                message: message,
                                response: response
                            }
                        ]
                    ]
                };
            }
        }),
    
    

    clearMessages: (sessionId) =>
        set((state) => ({
            sessions: state.sessions.map((session) =>
                session.sessionId === sessionId ? { ...session, messages: [] } : session
            ),
        })),

    hasMessages: (sessionId) => {
        const sessionIndex = get().sessions.findIndex((_, index) => index === sessionId);        
        return sessionIndex !== -1; // Return true if sessionIndex is not -1, indicating that the session was found
    },
    
    selectSession: (sessionId) => set({ selectedSessionId: sessionId }),

    getSelectedSessionId: () => {
        return get().selectedSessionId;
    },
}));

useMessageStore.getState().init();

export default useMessageStore;
