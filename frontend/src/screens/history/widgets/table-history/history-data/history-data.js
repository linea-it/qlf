import React from 'react';
import TableRow from '@material-ui/core/TableRow';
import TableCell from '@material-ui/core/TableCell';
import PropTypes from 'prop-types';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';
import Checkbox from '@material-ui/core/Checkbox';
import Icon from '@material-ui/core/Icon';
import moment from 'moment';

const styles = {
  link: {
    cursor: 'pointer',
    textDecoration: 'none',
  },
  bold: { fontWeight: 900 },
  tableCell: {
    padding: '4px',
    textAlign: 'center',
  },
  notificationsIcon: {
    cursor: 'pointer',
  },
  statusAbort: {
    color: 'red',
  },
  statusPending: {
    color: '#EFD469',
  },
  statusNormal: {
    color: 'green',
  },
  text: {
    fontSize: '1.2vw',
  },
  ico: {
    fontSize: '2vw',
  },
  normalTick: {
    color: 'green',
    textShadow: '0.5px 0.5px 0 gray, 0 0 0.5px gray, 0 0 0 gray',
  },
  errorTick: {
    color: 'red',
    textShadow: '0.5px 0.5px 0 gray, 0 0 0.5px gray, 0 0 0 gray',
  },
  warningTick: {
    color: '#ffeb3b',
    textShadow: '0.5px 0.5px 0 gray, 0 0 0.5px gray, 0 0 0 gray',
  },
};

class HistoryData extends React.Component {
  static muiName = 'TableRow';
  static propTypes = {
    processId: PropTypes.string,
    lastProcessedId: PropTypes.string,
    row: PropTypes.object,
    type: PropTypes.string,
    children: PropTypes.array,
    selectProcessQA: PropTypes.func.isRequired,
    selectedExposures: PropTypes.array,
    selectable: PropTypes.bool,
    selectExposure: PropTypes.func,
    rowNumber: PropTypes.number,
    displayBorder: PropTypes.bool,
    striped: PropTypes.bool,
    tableColumns: PropTypes.array.isRequired,
    handleCommentModalOpen: PropTypes.func.isRequired,
    pipelineRunning: PropTypes.string,
    openLogViewer: PropTypes.func,
    setAnchorEl: PropTypes.func.isRequired,
    classes: PropTypes.object.isRequired,
  };

  formatDate = date => {
    return moment(date).format('YYYYMMDD');
  };

  formatTime = dateString => {
    return moment(dateString).format('hh:mm:ss');
  };

  qaSuccess = () => {
    const { row } = this.props;
    const qaTests = row.qa_tests
      ? row.qa_tests
      : row.last_exposure_process_qa_tests
        ? row.last_exposure_process_qa_tests
        : null;
    if (!Array.isArray(qaTests)) return null;
    if (qaTests) {
      if (
        JSON.stringify(qaTests).includes('None') ||
        JSON.stringify(qaTests).includes('ALARM') ||
        JSON.stringify(qaTests).includes('FAIL')
      )
        return 0;
      if (JSON.stringify(qaTests).includes('WARNING')) {
        return 1;
      }
      return 2;
    }
    return 0;
  };

  renderQAStatus = status => {
    switch (status) {
      case 0:
        return <span style={styles.errorTick}>✖︎</span>;
      case 1:
        return <span style={styles.warningTick}>✖︎</span>;
      default:
        return <span style={styles.normalTick}>✓</span>;
    }
  };

  renderViewQA = (processing, runtime) => {
    if (processing && !runtime) return <CircularProgress size={20} />;

    return (
      <span
        style={styles.link}
        onClick={() => this.props.selectProcessQA(this.props.processId)}
      >
        {this.renderQAStatus(this.qaSuccess())}
      </span>
    );
  };

  renderStatus = state => {
    switch (state) {
      case 'aborted':
        return <span style={styles.statusAbort}>Aborted</span>;
      case 'failed':
        return <span style={styles.statusAbort}>Failed</span>;
      case 'pending':
        return <span style={styles.statusPending}>Pending</span>;
      case 'warning':
        return <span style={styles.statusPending}>Warning</span>;
      default:
        return <span style={styles.statusNormal}>Normal</span>;
    }
  };

  qaState = () => {
    switch (this.qaSuccess()) {
      case 0:
        return 'failed';
      case 1:
        return 'warning';
      default:
        return 'normal';
    }
  };

  renderColumns = (type, key, id) => {
    const { row, selectProcessQA, processId } = this.props;
    const isNotProcessingHistory = this.props.type !== 'process';
    const processing = isNotProcessingHistory
      ? null
      : this.props.lastProcessedId === String(row.pk) &&
        this.props.pipelineRunning &&
        this.props.pipelineRunning === 'Running';
    const lastProcessed = processing ? styles.bold : {};
    let comment;
    if (this.props.type === 'process') {
      comment = row.comments_count ? 'chat_bubble' : 'chat_bubble_outline';
    } else {
      comment = row.last_process_comments_count
        ? 'chat_bubble'
        : 'chat_bubble_outline';
    }

    const { classes } = this.props;
    const status = !row.runtime
      ? processing ? 'pending' : 'aborted'
      : this.qaState();
    const flavor = isNotProcessingHistory
      ? row['flavor']
      : row.exposure['flavor'];

    switch (type) {
      case 'parent':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {row[id]}
          </TableCell>
        );
      case 'normal':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {isNotProcessingHistory ? row[id] : row.exposure[id]}
          </TableCell>
        );
      case 'date':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {this.formatDate(
              isNotProcessingHistory ? row[id] : row.exposure[id]
            )}
          </TableCell>
        );
      case 'dateprocess':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {this.formatDate(row[id])}
          </TableCell>
        );
      case 'time':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {this.formatTime(
              isNotProcessingHistory ? row.dateobs : row.exposure.dateobs
            )}
          </TableCell>
        );
      case 'datemjd':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {row.datemjd.toFixed(3)}
          </TableCell>
        );
      case 'image':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            <Icon
              onClick={evt => this.props.setAnchorEl(evt, processId, flavor)}
              style={styles.notificationsIcon}
              classes={{ root: classes.ico }}
            >
              pageview
            </Icon>
          </TableCell>
        );
      case 'comments':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            <Icon
              onClick={() => this.props.handleCommentModalOpen(processId)}
              style={styles.notificationsIcon}
              classes={{ root: classes.ico }}
            >
              {comment}
            </Icon>
          </TableCell>
        );
      case 'runtime':
        return (
          <TableCell
            key={`EXPV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {!row.runtime && !processing ? '' : row.runtime}
          </TableCell>
        );
      case 'status':
        return (
          <TableCell
            key={`EXPV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {this.renderStatus(status)}
          </TableCell>
        );
      case 'qa':
        if (isNotProcessingHistory) {
          const { lastProcessedId } = this.props;
          const processed = lastProcessedId && lastProcessedId === processId;
          return (
            <TableCell
              key={`EXPV${key}`}
              style={{ ...styles.tableCell, ...lastProcessed }}
              classes={{ root: classes.text }}
            >
              {!processed && processId ? (
                <span
                  style={styles.link}
                  onClick={() => selectProcessQA(processId)}
                >
                  {this.renderQAStatus(this.qaSuccess())}
                </span>
              ) : null}
            </TableCell>
          );
        }
        if (!row.qa_tests || (!row.qa_tests.length && !processing))
          return <TableCell key={'err'} />;
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            {this.renderViewQA(processing, row.runtime)}
          </TableCell>
        );
      case 'log':
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          >
            <Icon
              onClick={() => this.props.openLogViewer(processId)}
              style={styles.notificationsIcon}
              classes={{ root: classes.ico }}
            >
              event_note
            </Icon>
          </TableCell>
        );
      default:
        return (
          <TableCell
            key={`PROCV${key}`}
            style={{ ...styles.tableCell, ...lastProcessed }}
            classes={{ root: classes.text }}
          />
        );
    }
  };

  renderProcessingHistory = () => {
    return (
      <TableRow>
        {this.props.tableColumns.map((column, key) => {
          const id = column.key.includes('exposure__')
            ? column.key.split('__')[1]
            : column.key;
          return this.renderColumns(column.type, key, id);
        })}
      </TableRow>
    );
  };

  renderCheckbox = checked => {
    if (!this.props.selectable) return;
    return (
      <TableCell style={{ ...styles.tableCell }}>
        <Checkbox checked={checked} />
      </TableCell>
    );
  };

  selectExposure = rowNumber => {
    if (this.props.selectExposure) this.props.selectExposure([rowNumber]);
  };

  renderObservingHistory = () => {
    const {
      processId,
      lastProcessedId,
      selectedExposures,
      rowNumber,
      striped,
    } = this.props;
    const lastProcessed =
      lastProcessedId && lastProcessedId === processId ? styles.bold : null;
    const selectedExposure =
      selectedExposures && selectedExposures.includes(rowNumber);

    return (
      <TableRow
        onClick={() => this.selectExposure(rowNumber)}
        style={lastProcessed}
        striped={striped}
      >
        {process.env.REACT_APP_OFFLINE === 'true'
          ? null
          : this.renderCheckbox(selectedExposure)}
        {this.props.tableColumns
          .filter(column => column.key !== null)
          .map((column, key) => {
            const id = column.key;
            return this.renderColumns(column.type, key, id);
          })}
      </TableRow>
    );
  };

  render() {
    return this.props.type === 'process'
      ? this.renderProcessingHistory()
      : this.renderObservingHistory();
  }
}

export default withStyles(styles)(HistoryData);
