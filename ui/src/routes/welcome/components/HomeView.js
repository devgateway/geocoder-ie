import React from 'react';
import './HomeView.scss';
import {Link} from 'react-router';

export const HomeView = () => (
  	<div>
	    <h4>Welcome to Autogeocoder</h4>
	    <div>
		    <Link to={'/classifier'}>Training Page</Link>
		</div>
		<div>    
			<Link to={'/docsManager'}>Document Manager</Link>
		</div>
	</div>
)

export default HomeView
