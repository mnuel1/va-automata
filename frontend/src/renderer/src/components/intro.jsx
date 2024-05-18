import Logo from '../assets/logo_no_text.png'


const Intro = () => {

    return (
        
        <div className='flex lg:flex-col justify-center items-center lg:gap-4 mt-16'>
            <img src={Logo} alt="logo no text" className=''/>
            <h1 className='text-white text-xl lg:text-3xl'>Hello, Manuel Marin! <br/> How can I help you today?</h1>
        </div>
    )

}

export default Intro