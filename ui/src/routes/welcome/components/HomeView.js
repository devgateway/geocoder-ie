import React from 'react';
import './HomeView.scss';
import {Link} from 'react-router';

export const HomeView = () => (
  	<div className="welcome-page">
	    <h1>Welcome to Autogeocoder</h1>
	    <div>
		    <Link to={'/classifier'}>Training Page</Link>
		</div>
		<div>    
			<Link to={'/docsManager'}>Document Manager</Link>
		</div>
	</div>
)

export default HomeView
