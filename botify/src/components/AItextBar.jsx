import React, { useState } from 'react';
import Groq from "groq-sdk";

const msgArray = [
    {
        id: 1,
        text: "hello world, this is my first text"
    }
];

function AItextBar({ messageList, setMessageList }) {
    const [inputText, setInputText] = useState('');
    const [loading, setLoading] = useState(false);

    // const handleSubmit = async () => {
    //     if (!inputText.trim()) return;
    //     const formattedInput = {
    //         type: 'user',
    //         text: inputText,
    //         timestamp: `${new Date().getHours()} : ${new Date().getMinutes()}`
    //     }
 
    //     setLoading(true);

    //     const newMessageList = [...messageList, formattedInput];
    //     setMessageList(newMessageList);
    //     try {
    //         const groq = new Groq({
    //             apiKey: import.meta.env.VITE_GROQ_API_KEY,
    //             dangerouslyAllowBrowser: true
    //         });

    //         const chatCompletion = await groq.chat.completions.create({
    //             messages: [
    //                 {
    //                     role: "user",
    //                     content: inputText
    //                 }
    //             ],
    //             model: "llama-3.2-11b-vision-preview",
    //             temperature: 1,
    //             max_tokens: 1024,
    //             top_p: 1,
    //             stream: false,
    //             stop: null
    //         });


    //         const response = chatCompletion.choices[0].message.content;

    //         const formattedResponse = {
    //             type: 'ai',
    //             name: 'Cosima AI',
    //             text: response,
    //             timestamp: `${new Date().getHours()}:${new Date().getMinutes()}`,
    //             avatar: '/api/placeholder/32/32'
    //         }

    //         setMessageList([...newMessageList, formattedResponse])
    //         setInputText(''); // Clear input after successful submission

    //     } catch (error) {
    //         alert(`Error: ${error.message || 'Failed to get response'}`);
    //     } finally {
    //         setLoading(false);
    //     }
    // };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className='w-full h-full rounded-3xl border-[1px] border-gray-400 flex gap-x-4 items-center px-4 justify-between py-2'>
            <div className='border-r-[2px] border-r-gray-400 flex gap-x-4 pr-4'>
                <div className='w-[32px] h-[32px] rounded-full flex items-center pl-[2.5px] group'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="25px" viewBox="0 -960 960 960" width="25px" fill="#d37abc">
                        <path d="M720-330q0 104-73 177T470-80q-104 0-177-73t-73-177v-370q0-75 52.5-127.5T400-880q75 0 127.5 52.5T580-700v350q0 46-32 78t-78 32q-46 0-78-32t-32-78v-370h80v370q0 13 8.5 21.5T470-320q13 0 21.5-8.5T500-350v-350q-1-42-29.5-71T400-800q-42 0-71 29t-29 71v370q-1 71 49 120.5T470-160q70 0 119-49.5T640-330v-390h80v390Z"
                            className='group-hover:fill-[#7642fe] group-hover:transition-all duration-500' />
                    </svg>
                </div>

                <div className='w-[32px] h-[32px] rounded-full flex items-center pl-[2.5px] group'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="25px" viewBox="0 -960 960 960" width="25px" fill="#d37abc">
                        <path d="M360-400h400L622-580l-92 120-62-80-108 140Zm-40 160q-33 0-56.5-23.5T240-320v-480q0-33 23.5-56.5T320-880h480q33 0 56.5 23.5T880-800v480q0 33-23.5 56.5T800-240H320Zm0-80h480v-480H320v480ZM160-80q-33 0-56.5-23.5T80-160v-560h80v560h560v80H160Zm160-720v480-480Z"
                            className='group-hover:fill-[#7642fe] group-hover:transition-all duration-500' />
                    </svg>
                </div>
            </div>

            <input
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder='Feeling Curious ?'
                disabled={loading}
                className='bg-gray-900 w-full focus:outline-none'
            />

            <button
                onClick={handleSubmit}
                disabled={loading || !inputText.trim()}
                className='bg-[#d37abc] w-[28px] h-[28px] rounded-full flex items-center pl-[2.5px] -rotate-45 hover:bg-[#7642fe] hover:w-[32px] hover:h-[32px] group disabled:opacity-50 disabled:hover:bg-[#d37abc] disabled:hover:w-[28px] disabled:hover:h-[28px]'
            >
                <svg xmlns="http://www.w3.org/2000/svg" height="26px" viewBox="0 -960 960 960" width="26px" fill="#111827">
                    <path d="M120-160v-640l760 320-760 320Zm80-120 474-200-474-200v140l240 60-240 60v140Zm0 0v-400 400Z"
                        className='group-hover:fill-[white] transition-all duration-500' />
                </svg>
            </button>
        </div>
    );
}

export default AItextBar;