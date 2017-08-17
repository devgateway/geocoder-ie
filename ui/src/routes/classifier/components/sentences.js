import PropTypes from 'prop-types'
import React,{Component} from 'react';
import ReactPaginate from 'react-paginate';
import './sentences.scss'


const Label=(props)=>(<div>{props.value?props.value:'N/A'}</div>)
const Delete=(props)=>(<div><input type='button' value='Delete' className='delete' onClick={props.onClick}/></div>)
const Geo=(props)=>(<div><input type='button' className='geo' value='Geography'  onClick={props.onClick}/></div>)
const None=(props)=>(<div><input type='button' className='none' value='None'  onClick={props.onClick}/></div>)
const Null=(props)=>(<div><input type='button' className='none' value='Unset'  onClick={props.onClick}/></div>)

const Option=(props)=>(<option  value={props.value}>{props.value}</option>)

export default class Sentences extends Component {

  componentWillMount() {
    this.props.onLoad();
    this.props.onLoadDocs();
  }

    render() {
      const {rows=[], onPageClick, count, limit, onUpdate, onDelete, onSearchChange, term, onSearch, docs=[], doc, onChangeDocument, onChangeCategory, category}=this.props
      const pageCount=count/limit
        return (
          <div className='corpora' style={{ margin: '0 auto' }} >
            <h1>Training Data  </h1>
            <h3>{count} Records  </h3>

            <div className="search-form">
                <div className="search-row">
                  <select onChange={e=>onChangeDocument(e.target.value)} value={doc}>
                    <Option value='All' current={doc}/>
                    {docs.map(d=><Option key={d.split('/')[d.split('/').length-1]} value={d.split('/')[d.split('/').length-1]}/>)}
                  </select>
                </div>
                <div className="search-row">
                  <input type="text" className="input-search" onChange={e=>onSearchChange(e.target.value)} value={term}/>
                </div>
                <input type="checkbox" value={category==='geography'? 'on' : 'off'} onChange={e=>onChangeCategory(e.target.value === 'off'? 'geography' : null)}/>
                <label>Show Only Geography</label>
                <div className="search-row right">
                    <input type='button' className='btn-search' value='Search'  onClick={onSearch}/>
                </div>
                
            </div>

                <ReactPaginate
                           previousLabel={"previous"}
                           nextLabel={"next"}
                           breakLabel={<a href="">...</a>}
                           breakClassName={"break-me"}
                           pageCount={pageCount}
                           onPageChange={(page,count,limit)=>{onPageClick(page.selected)}}
                           containerClassName={"pagination"}
                           subContainerClassName={"pages pagination"}
                           activeClassName={"active"} />
            <table>
            <tbody>
            {(rows)?rows.map(l=><tr className={l[2]} key={l[0]}>
                                    <td>{l[0]}</td>
                                    <td>{l[1]}</td>
                                    <td><Label value={l[2]}/></td>
                                    <td><Geo value={l[2]} onClick={e=>onUpdate(l[0],'geography')}/></td>
                                    <td><None value={l[2]} onClick={e=>onUpdate(l[0],'none')}/></td>
                                    <td><Null value={l[2]} onClick={e=>onUpdate(l[0],'')}/></td>
                                    <td><Delete value={l[2]} onClick={e=>onDelete(l[0])}/></td>
                                    <td><a target='new' href={`${window.API_ROOT}/download/${l[0]}`}>{l[3].split('/').pop()}</a></td>
                                </tr>):null}


            </tbody>
            </table>
            <ReactPaginate
                       previousLabel={"previous"}
                       nextLabel={"next"}
                       breakLabel={<a href="">...</a>}
                       breakClassName={"break-me"}
                       pageCount={pageCount}
                       onPageChange={(page,count,limit)=>{onPageClick(page.selected)}}
                       containerClassName={"pagination"}
                       subContainerClassName={"pages pagination"}
                       activeClassName={"active"} />
          </div>
        );
    }
}
