import Logo from '../assets/logo_no_text.png'


const Intro = () => {

    return (
        
        <div className='flex flex-col justify-center items-center gap-4'>
            <img src={Logo} alt="logo no text" />
            <h1 className='text-white text-3xl'>Hello, Manuel Marin! <br/> How can I help you today?</h1>
        </div>
    )

}

export default Intro