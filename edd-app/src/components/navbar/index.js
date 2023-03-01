import React from 'react';

import {
  Nav,
  NavLink,
  Bars,
  NavMenu,
  NavBtn,
  NavBtnLink,
} from './NavbarElements';
  
function Navbar(props) {
    var login_state = props.loggedIn ? "Log Out" : "Log In"
    var logout_func = props.logout
    return (
    <>
        <Nav>
        <Bars />
  
        <NavMenu>
            <NavLink to='/dashboard' activeStyle>
                Dashboard
            </NavLink>
            <NavLink to='/register' activeStyle>
                Register
            </NavLink>
            {/* Second Nav */}
            {/* <NavBtnLink to='/sign-in'>Sign In</NavBtnLink> */}
        </NavMenu>
        <NavLink to='/' onClick={logout_func} activeStyle>
            {login_state}
        </NavLink>
        </Nav>
    </>
    );
};
  
export default Navbar;